# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug


class WebsiteServiceController(http.Controller):
    
    @http.route(['/service/<model("website.service"):service>'], 
                type='http', auth="public", website=True, sitemap=True)
    def service_detail(self, service, **kwargs):
        """Display individual service detail page"""
        
        # Ensure the service is published
        if not service.website_published:
            return request.redirect('/404')
        
        values = {
            'service': service,
            'main_object': service,
        }
        
        return request.render('website_service.service_detail_template', values)