from odoo import models, fields


class WebsiteProjects(models.Model):
    _name = "website.projects"
    _inherit = 'multi.themes.base.mixin'
    _order = "sequence, id"

    website_image = fields.Binary("Project Website Image")
    title = fields.Char("Project Title", translate=True)
    sub_title = fields.Text("Project Sub Title", translate=True)
    teaser = fields.Text("Project Teaser", translate=True)
    desc = fields.Html("Project Description", translate=True)
    sequence = fields.Integer("Sequence", default=10)
