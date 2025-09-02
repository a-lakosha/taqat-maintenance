# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class WebsiteServiceTag(models.Model):
    _name = 'website.service.tag'
    _description = 'Service Tag'
    _order = 'sequence, name'
    _rec_name = 'name'
    
    name = fields.Char(
        string='Tag Name', 
        required=True, 
        translate=True
    )
    icon = fields.Char(
        string='Icon Class',
        help="CSS class for the icon (e.g., 'fa fa-star' or 'bi bi-star')"
    )
    color = fields.Integer(
        string='Color Index',
        default=0,
        help="Color index for the tag"
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Gives the sequence order when displaying a list of tags."
    )
    service_ids = fields.Many2many(
        'website.service',
        'website_service_tag_rel',
        'tag_id',
        'service_id',
        string='Services'
    )
    service_count = fields.Integer(
        string='Number of Services',
        compute='_compute_service_count'
    )
    
    @api.depends('service_ids')
    def _compute_service_count(self):
        for record in self:
            record.service_count = len(record.service_ids)