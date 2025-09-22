# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class WebsiteServiceType(models.Model):
    _name = 'website.service.type'
    _description = 'Service Type'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(
        string='Type Name',
        required=True,
        translate=True
    )
    description = fields.Text(
        string='Description',
        translate=True
    )
    service_ids = fields.One2many(
        'website.service',
        'type_id',
        string='Services'
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Gives the sequence order when displaying a list of types."
    )
    service_count = fields.Integer(
        string='Number of Services',
        compute='_compute_service_count'
    )

    @api.depends('service_ids')
    def _compute_service_count(self):
        for record in self:
            record.service_count = len(record.service_ids)

    @api.model
    def _generate_service_menus(self):
        """Generate dynamic menu items for service types and services"""
        print("=== Starting _generate_service_menus ===")

        # Work with both theme and website menus
        ThemeMenuModel = self.env['theme.website.menu']
        WebsiteMenuModel = self.env['website.menu']
        website = self.env['website'].browse(1)  # Default website

        print(f"DEBUG: Using website: {website.name}")

        # Get the main Services menu (theme menu)
        services_theme_menu = self.env.ref('theme_maintenance.menu_services', raise_if_not_found=False)
        print(
            f"DEBUG: services_theme_menu = {services_theme_menu}, ID = {services_theme_menu.id if services_theme_menu else 'None'}")
        if not services_theme_menu:
            print("DEBUG: No services menu found!")
            return

        # Find the corresponding website menu
        services_website_menu = services_theme_menu.copy_ids.filtered(lambda x: x.website_id == website)
        print(
            f"DEBUG: services_website_menu = {services_website_menu}, ID = {services_website_menu.id if services_website_menu else 'None'}")

        # Remove ALL existing service-related menus from BOTH theme and website menus
        # First, find all service type names to identify which menus to remove
        all_service_type_names = self.search([]).mapped('name')
        print(f"DEBUG: All service type names: {all_service_type_names}")

        # Remove theme menus (children of services menu)
        existing_theme_menus = ThemeMenuModel.search([
            ('parent_id', '=', services_theme_menu.id),
            ('name', '!=', 'Services')
        ])
        print(f"DEBUG: Found {len(existing_theme_menus)} existing theme menus to remove")

        # Remove their website menu copies first
        for theme_menu in existing_theme_menus:
            website_copies = theme_menu.copy_ids.filtered(lambda x: x.website_id == website)
            if website_copies:
                print(f"DEBUG: Removing website menu copies: {[m.name for m in website_copies]}")
                website_copies.unlink()

        # Remove theme menus
        existing_theme_menus.unlink()

        # Also remove any orphaned website menus that might be service-related
        if services_website_menu:
            orphaned_website_menus = WebsiteMenuModel.search([
                ('parent_id', '=', services_website_menu.id),
                ('name', 'in', all_service_type_names + [s.name for s in self.env['website.service'].search([])])
            ])
            if orphaned_website_menus:
                print(
                    f"DEBUG: Found {len(orphaned_website_menus)} orphaned website menus to remove: {[m.name for m in orphaned_website_menus]}")
                orphaned_website_menus.unlink()

            # Also remove any nested service menus
            all_service_website_menus = WebsiteMenuModel.search([
                ('parent_id', 'child_of', services_website_menu.id),
                ('id', '!=', services_website_menu.id)
            ])
            if all_service_website_menus:
                print(f"DEBUG: Removing all nested service menus: {[m.name for m in all_service_website_menus]}")
                all_service_website_menus.unlink()

        # Clean up duplicate main menu items (Home, About, Blogs, etc.)
        print("DEBUG: Cleaning up duplicate main menu items")
        main_website_menu = website.menu_id
        if main_website_menu:
            duplicate_check = {}
            main_menu_children = WebsiteMenuModel.search([('parent_id', '=', main_website_menu.id)])

            for menu_item in main_menu_children:
                menu_name = menu_item.name.strip()
                if menu_name in duplicate_check:
                    print(f"DEBUG: Found duplicate menu '{menu_name}' - removing ID {menu_item.id}")
                    menu_item.unlink()
                else:
                    duplicate_check[menu_name] = menu_item.id

        # Get all service types with their services
        service_types = self.search([])
        print(f"DEBUG: Found {len(service_types)} service types: {[st.name for st in service_types]}")

        for sequence, service_type in enumerate(service_types, 1):
            print(f"DEBUG: Processing service type '{service_type.name}' with {len(service_type.service_ids)} services")

            # Create theme menu for service type (always without URL to make it a dropdown)
            type_menu_vals = {
                'name': service_type.name,
                'parent_id': services_theme_menu.id,
                'sequence': sequence * 10,
                # No URL - this makes it a dropdown parent
            }

            if len(service_type.service_ids) == 0:
                print("DEBUG: No services for this type - creating dropdown without items")
            else:
                print(
                    f"DEBUG: Creating dropdown for '{service_type.name}' with {len(service_type.service_ids)} services")

            try:
                # Create theme menu (always a dropdown parent)
                theme_type_menu = ThemeMenuModel.create(type_menu_vals)
                print(f"DEBUG: Created theme type menu with ID {theme_type_menu.id}")

                # Convert to website menu immediately
                menu_data = theme_type_menu._convert_to_base_model(website)
                if menu_data:
                    website_type_menu = WebsiteMenuModel.create(menu_data)
                    print(f"DEBUG: Created website type menu with ID {website_type_menu.id}")

                    # Create submenus for ALL services (whether 1 or many)
                    if len(service_type.service_ids) > 0:
                        for sub_sequence, service in enumerate(service_type.service_ids, 1):
                            # Create theme submenu
                            service_theme_menu_vals = {
                                'name': service.tec_name or service.name,
                                'url': f'/service/{service.id}',
                                'parent_id': theme_type_menu.id,
                                'sequence': sub_sequence * 10,
                            }
                            theme_service_menu = ThemeMenuModel.create(service_theme_menu_vals)
                            print(
                                f"DEBUG: Created theme service submenu '{service.tec_name or service.name}' with ID {theme_service_menu.id}")

                            # Convert to website submenu
                            service_menu_data = theme_service_menu._convert_to_base_model(website)
                            if service_menu_data:
                                website_service_menu = WebsiteMenuModel.create(service_menu_data)
                                print(
                                    f"DEBUG: Created website service submenu '{service.tec_name or service.name}' with ID {website_service_menu.id}")

            except Exception as e:
                print(f"DEBUG: Error creating menu: {e}")

        print("=== DEBUG: Finished _generate_service_menus ===")

    @api.model
    def debug_manual_generate_menus(self):
        """Manual method to trigger menu generation for testing"""
        print("DEBUG: Manual menu generation triggered")
        return self._generate_service_menus()

    @api.model_create_multi
    def create(self, vals_list):
        """Regenerate menus when service types are created"""
        print("DEBUG: Service type CREATE called - will regenerate menus")
        result = super().create(vals_list)
        self._generate_service_menus()
        return result

    def write(self, vals):
        """Regenerate menus when service types are updated"""
        print(f"DEBUG: Service type WRITE called with vals: {vals}")
        result = super().write(vals)
        if 'name' in vals or 'sequence' in vals:
            print("DEBUG: Name or sequence changed - will regenerate menus")
            self._generate_service_menus()
        return result

    def unlink(self):
        """Regenerate menus when service types are deleted"""
        result = super().unlink()
        self._generate_service_menus()
        return result
