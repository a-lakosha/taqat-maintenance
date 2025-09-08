from odoo import models, fields


class WebsiteSuccessStories(models.Model):
    _name = "website.success.stories"
    _inherit = 'multi.themes.base.mixin'
    _order = "sequence, id"

    image = fields.Binary("Image", required=True)
    title = fields.Char("Title", required=True, translate=True)
    description = fields.Html("Description", translate=True)
    name = fields.Text("Name", translate=True)
    job_title = fields.Text("Job Title", translate=True)
    sequence = fields.Integer("Sequence", default=15)
