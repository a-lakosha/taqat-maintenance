from odoo import models, fields


class WebsiteFaqs(models.Model):
    _name = "website.faqs"
    _inherit = 'multi.themes.base.mixin'
    _order = "sequence, id"

    title = fields.Char("Title", translate=True)
    description = fields.Text("Description", translate=True)
    sequence = fields.Integer("Sequence", default=10)
