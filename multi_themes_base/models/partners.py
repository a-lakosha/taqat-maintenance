from odoo import models, fields


class WebsitePartners(models.Model):
    _name = "website.partners"
    _inherit = 'multi.themes.base.mixin'
    _order = "sequence, id"

    name = fields.Char('Partner Name', translate=True)
    image = fields.Binary('Image', store=True)
    sequence = fields.Integer('Sequence', default=10)
