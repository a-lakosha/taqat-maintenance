from odoo import models, fields


class HrJob(models.Model):
    _inherit = 'hr.job'

    date_jobs = fields.Date(string="Job Date")
    experience = fields.Integer(string="Experience Required")
    view_Positions_carers = fields.Boolean(string="view Position Carers")
