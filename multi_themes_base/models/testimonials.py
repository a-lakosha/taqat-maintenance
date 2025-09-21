from odoo import models, fields


class WebsiteTeam(models.Model):
    _name = 'testimonials.model'
    _inherit = 'multi.themes.base.mixin'
    _description = 'Testimonials team'

    img_url = fields.Binary('image')
    name = fields.Char('name', translate=True)
    description = fields.Char('Description', translate=True)
    rating = fields.Selection([
        ('0.5', '.5 Star'),
        ('1', '1 Star'),
        ('1.5', '1.5 Star'),
        ('2', '2 Star'),
        ('2.5', '2.5 Star'),
        ('3', '3 Star'),
        ('3.5', '3.5 Star'),
        ('4', '4 Star'),
        ('4.5', '4.5 Star'),
        ('5', '5 Star'),
    ])
    job_title = fields.Char('Jop Title', translate=True)
    sequence = fields.Integer("Sequence", default=10)
