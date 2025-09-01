# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.tools.translate import html_translate


class WebsiteService(models.Model):
    _name = 'website.service'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin',
                'website.seo.metadata', 'website.published.multi.mixin', 
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
    tag_ids = fields.Many2many(
        'website.service.tag',
        'website_service_tag_rel',
        'service_id',
        'tag_id',
        string='Tags'
    )

    # Website fields
    website_id = fields.Many2one(
        'website',
        string='Website',
        ondelete='restrict',
        default=lambda self: self.env['website'].search([('company_id', '=', self.env.company.id)], limit=1),
        help="Restrict publishing to a specific website."
    )

    def _get_default_website_description(self):
        """Return default HTML template for service description"""
        return '''
            <section class="container my-5">
                <!-- Hero Section -->
                <div class="row mb-5">
                    <div class="col-12">
                        <h2 class="display-6 fw-bold mb-3">Clean Spaces... Strong Impressions</h2>
                        <p class="lead">Professional cleaning services tailored to your needs.</p>
                        <a href="/contactus" class="btn btn-warning btn-lg">Ask for service →</a>
                    </div>
                </div>
                
                <!-- Why Us Section -->
                <div class="row mb-5">
                    <div class="col-12 text-center mb-4">
                        <h6 class="text-warning fw-bold">Why us</h6>
                        <h3 class="fw-bold">What sets us apart in providing....</h3>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="text-center">
                            <i class="bi bi-check-circle fs-1 text-warning mb-3"></i>
                            <h5>Responsiveness</h5>
                            <p>Quick response to all service requests with professional handling.</p>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="text-center">
                            <i class="bi bi-people fs-1 text-warning mb-3"></i>
                            <h5>Specialized teams</h5>
                            <p>Expert teams trained for specific cleaning requirements.</p>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="text-center">
                            <i class="bi bi-clipboard-data fs-1 text-warning mb-3"></i>
                            <h5>Regular reports</h5>
                            <p>Detailed reports on service quality and progress.</p>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="text-center">
                            <i class="bi bi-gem fs-1 text-warning mb-3"></i>
                            <h5>Material quality</h5>
                            <p>Premium quality cleaning materials and equipment.</p>
                        </div>
                    </div>
                </div>
                
                <!-- FAQ Section -->
                <div class="row mb-5">
                    <div class="col-lg-8 mx-auto text-center">
                        <p class="text-muted small">The value of the service to the beneficiary</p>
                        <h4 class="fw-bold mb-4">How does this service contribute to real estate preservation?</h4>
                        <p>Our professional cleaning services help maintain property value by ensuring regular maintenance, preventing deterioration, and creating positive impressions for tenants and visitors.</p>
                    </div>
                </div>
                
                <!-- Info Cards -->
                <div class="row">
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title fw-bold">Lorem Ipsum dolor</h5>
                                <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title fw-bold">Lorem Ipsum dolor</h5>
                                <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title fw-bold">Lorem Ipsum dolor</h5>
                                <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        '''

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
            'base_domain': [website.website_domain(), ('website_published', '=', True)],
            'search_fields': search_fields,
            'fetch_fields': fetch_fields,
            'mapping': mapping,
            'icon': 'fa-wrench',
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
