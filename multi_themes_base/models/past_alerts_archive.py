from odoo import models, fields


class WebsitePastAlertsArchive(models.Model):
    _name = "website.past.alerts.archive"
    _inherit = 'multi.themes.base.mixin'
    _order = "sequence, id"

    image = fields.Binary("Disaster Image")
    name = fields.Char("Disaster Name", translate=True)
    affected_areas = fields.Text("Affected Areas", translate=True)
    affected_areas_description = fields.Text("Affected Areas Description", translate=True)
    size_of_intervention = fields.Char("Size of Intervention")
    number_of_beneficiaries = fields.Char("Number of Beneficiaries")
    
    sequence = fields.Integer("Sequence", default=15)
