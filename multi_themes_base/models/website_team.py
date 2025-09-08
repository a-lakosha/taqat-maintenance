from odoo import models, fields


class WebsiteTeam(models.Model):
    _name = 'website.team'
    _inherit = 'multi.themes.base.mixin'
    _description = 'website team'
    _order = "sequence, id"
    
    img_url = fields.Binary('image')
    name = fields.Char('name', translate=True)
    job_title = fields.Char('Jop Title', translate=True)
    sequence = fields.Integer("Sequence", default=10)
