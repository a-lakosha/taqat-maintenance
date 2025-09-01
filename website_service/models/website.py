# -*- coding: utf-8 -*-
from odoo import models, _


class Website(models.Model):
    _inherit = "website"

    def get_suggested_controllers(self):
        """Add service controller to suggested controllers"""
        suggested_controllers = super(Website, self).get_suggested_controllers()
        suggested_controllers.append(
            (_('Website Service'), self.env['ir.http']._url_for('/services'), 'website_service'))
        return suggested_controllers

    def get_cta_data(self, website_purpose, website_type):
        """Add CTA data for website service"""
        cta_data = super(Website, self).get_cta_data(website_purpose, website_type)
        if website_purpose == 'website_service':
            cta_data.update({
                'cta_btn_text': _('View Services'),
                'cta_btn_href': '/services',
            })
        return cta_data

    def configurator_set_menu_links(self, menu_company, module_data):
        """Create menu links for services"""
        services = module_data.get('#service', [])
        for idx, service in enumerate(services):
            new_service = self.env['website.service'].create({
                'name': service['name'],
                'website_id': self.id,
                'description': service.get('description', ''),
            })
            service_menu_values = {
                'name': service['name'],
                'url': '/service/%s' % new_service.id,
                'sequence': service.get('sequence', 10),
                'parent_id': menu_company.id if menu_company else self.menu_id.id,
                'website_id': self.id,
            }
            if idx == 0:
                # Update existing service menu if it exists
                service_menu = self.env['website.menu'].search([
                    ('url', '=', '/services'),
                    ('website_id', '=', self.id)
                ])
                if service_menu:
                    service_menu.write(service_menu_values)
                else:
                    self.env['website.menu'].create(service_menu_values)
            else:
                self.env['website.menu'].create(service_menu_values)

        return super().configurator_set_menu_links(menu_company, module_data)

    def _search_get_details(self, search_type, order, options):
        """Add services to website search"""
        result = super()._search_get_details(search_type, order, options)
        if search_type in ['services', 'all']:
            result.append(self.env['website.service']._search_get_detail(self, order, options))
        return result