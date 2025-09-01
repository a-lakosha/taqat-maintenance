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