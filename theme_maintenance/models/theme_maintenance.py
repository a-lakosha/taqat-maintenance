from odoo import models


class ThemeMaintenance(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_maintenance_post_copy(self, mod):
        self.disable_view('website_blog.opt_blog_post_breadcrumb')
        self.enable_view('website_blog.opt_blog_post_regular_cover')
        self.disable_view('website_blog.opt_blog_post_readable')
        self.disable_view('website_blog.opt_blog_cover_post_fullwidth_design')
        self.disable_view('website.footer_custom')
