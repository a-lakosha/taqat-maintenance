from odoo import models, fields


class WebsitePrograms(models.Model):
    _name = "website.programs"
    _inherit = 'multi.themes.base.mixin'
    _order = "sequence, id"

    logo = fields.Binary("Program Logo")
    website_image = fields.Binary("Program Website Image")
    title = fields.Char("Program Label", translate=True)
    desc = fields.Text("Program Description", translate=True)
    details = fields.Text("Program Details", translate=True)
    href = fields.Char("Program Href")
    sequence = fields.Integer("Sequence", default=10)
