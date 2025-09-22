from odoo import models


class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    def _validate_parent_menu(self):
        # Disable the 2-level validation
        return True
