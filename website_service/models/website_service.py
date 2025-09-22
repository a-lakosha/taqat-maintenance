# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.tools.translate import html_translate
from odoo.tools import mute_logger


class WebsiteService(models.Model):
    _name = 'website.service'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin',
                'website.seo.metadata', 'website.published.multi.mixin',
                'website.cover_properties.mixin',
                'website.searchable.mixin']
    _description = 'Service'
    _order = 'sequence, id'
    _rec_name = 'name'

    name = fields.Char(
        string='Service Name',
        required=True,
        translate=True,
        tracking=True
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Gives the sequence order when displaying a list of services."
    )
    tec_name = fields.Text(
        string='Technical Name',
        translate=True,
        help="Brief description of the service"
    )
    icon = fields.Char(
        string='SVG Icon',
        help="SVG code for the icon (e.g., '<svg>...</svg>')",
    )
    description = fields.Text(
        string='Short Description',
        translate=True,
        help="Brief description of the service"
    )
    website_description = fields.Html(
        string='Website Description',
        translate=html_translate,
        sanitize_attributes=False,
        default=lambda self: self._get_default_website_description(),
        help="Full description to be displayed on the website"
    )
    type_id = fields.Many2one(
        'website.service.type',
        string='Service Type',
        ondelete='restrict'
    )
    # Website fields
    website_id = fields.Many2one(
        'website',
        string='Website',
        ondelete='restrict',
        default=lambda self: self.env['website'].search([('company_id', '=', self.env.company.id)], limit=1),
        help="Restrict publishing to a specific website."
    )

    @mute_logger('odoo.addons.base.models.ir_qweb')
    def _get_default_website_description(self):
        return self.env['ir.qweb']._render("website_service.default_website_description",
                                           raise_if_not_found=False)

    @api.depends('name')
    def _compute_website_url(self):
        super(WebsiteService, self)._compute_website_url()
        for service in self:
            if service.id:
                service.website_url = "/service/%s" % slug(service)
            else:
                service.website_url = "#"

    def open_website_url(self):
        """Open the service page on the website"""
        return self.env['website'].get_client_action(self.website_url)

    @api.model
    def _search_get_detail(self, website, order, options):
        """Define search configuration for website search"""
        with_description = options.get('displayDescription', True)
        search_fields = ['name']
        fetch_fields = ['id', 'name']
        mapping = {
            'name': {'name': 'name', 'type': 'text', 'match': True},
            'website_url': {'name': 'url', 'type': 'text', 'truncate': False},
        }
        if with_description:
            search_fields.append('description')
            fetch_fields.append('description')
            mapping['description'] = {'name': 'description', 'type': 'text', 'match': True}

        return {
            'model': 'website.service',
            'base_domain': [],
            'search_fields': search_fields,
            'fetch_fields': fetch_fields,
            'mapping': mapping,
            'icon': 'fa-gears',
            'order': 'name desc, id desc' if 'name desc' in order else 'name asc, id desc',
        }

    def _search_render_results(self, fetch_fields, mapping, icon, limit):
        """Customize search result URLs"""
        results_data = super()._search_render_results(fetch_fields, mapping, icon, limit)
        for data in results_data:
            data['url'] = '/service/%s' % slug(self.browse(data['id']))
        return results_data

    def _default_website_meta(self):
        res = super(WebsiteService, self)._default_website_meta()
        res['default_opengraph']['og:description'] = res['default_twitter']['twitter:description'] = self.description
        res['default_opengraph']['og:type'] = 'article'
        res['default_opengraph']['og:title'] = res['default_twitter']['twitter:title'] = self.name
        res['default_opengraph']['og:image'] = res['default_twitter']['twitter:image'] = self.env['website'].image_url(
            self, 'image_1920')
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """Regenerate menus when services are created"""
        result = super().create(vals_list)
        self.env['website.service.type']._generate_service_menus()
        return result

    def write(self, vals):
        """Regenerate menus when services are updated"""
        result = super().write(vals)
        if 'name' in vals or 'type_id' in vals or 'sequence' in vals:
            self.env['website.service.type']._generate_service_menus()
        return result

    def unlink(self):
        """Regenerate menus when services are deleted"""
        result = super().unlink()
        self.env['website.service.type']._generate_service_menus()
        return result
