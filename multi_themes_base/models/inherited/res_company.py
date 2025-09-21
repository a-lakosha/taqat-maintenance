from odoo import api, fields, models
import base64
from io import BytesIO


class ResCompany(models.Model):
    _inherit = 'res.company'

    multi_website_filter = fields.Selection([
        ('taqat', 'Taqat'),
        ('maintenance', 'Taqat Maintenance'),
        ('edama', 'Edama'),
        ('tawridat', 'Tawridat'),
        ('pearl_pixels', 'Pearl Pixels'),
        ('relief_center', 'Relief Center'),
        ('avrasya', 'Avrasya'),
        ('taqatechno', 'TaqaTechno'),
        ('indoqat', 'Indoqat'),
    ])
