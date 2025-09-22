from odoo import models

class WebsiteMenu(models.Model):
    _inherit = 'website.menu'

    def _check_menu_hierarchy(self):
        """Override to allow more than 2 levels of menu hierarchy"""
        # Skip the original validation by returning True
        return True