from odoo import models, fields, api, _


class Inherit(models.Model):
    _inherit = 'blog.post'

    is_featured = fields.Boolean(string='Featured post checkbox')
