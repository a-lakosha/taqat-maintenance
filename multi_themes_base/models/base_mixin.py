from odoo import models, fields, api, _
from odoo.http import request
from odoo.exceptions import ValidationError


class MultiThemesBaseMixin(models.AbstractModel):
    """Base mixin for all multi_themes_base models to handle company and website defaults properly"""
    _name = 'multi.themes.base.mixin'
    _description = 'Multi Themes Base Mixin'

    def _default_company(self):
        """Get default company from context or current user's company"""
        # Check if company_id is passed in context
        if self._context.get('default_company_id'):
            company_id = self._context['default_company_id']
            company = self.env['res.company'].browse(company_id)
            return company
        
        # Otherwise use current user's company
        return self.env.company

    def _default_website(self):
        """Get default website based on company and context"""
        # First check if we're in a website context (frontend request)
        if request and hasattr(request, 'website'):
            return request.website
        
        # Check if website_id is passed in context
        if self._context.get('default_website_id'):
            website_id = self._context['default_website_id']
            return self.env['website'].browse(website_id)
        
        # Get the company (either from context or current user)
        company = self._default_company()
        
        # Search for first website of this company
        website = self.env['website'].search([
            ('company_id', '=', company.id)
        ], limit=1)
        
        if website:
            return website
        
        # If no website found for company, try to get current website
        current_website = self.env['website'].get_current_website(fallback=False)
        if current_website:
            return current_website
        
        # Last resort: return any website
        return self.env['website'].search([], limit=1)

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=_default_company,
        required=True,
        help="Company to which this record belongs"
    )
    
    website_id = fields.Many2one(
        'website',
        string='Website',
        default=_default_website,
        domain="[('company_id', '=', company_id)]",
        help="Website to which this record is published. Leave empty to publish on all websites."
    )
    
    company_filter = fields.Selection(
        related='company_id.multi_website_filter',
        store=False,
        help="Filter type from company configuration"
    )
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to ensure company and website are always properly set"""
        for vals in vals_list:
            # FORCE company_id if not provided or invalid
            if not vals.get('company_id'):
                default_company = self._default_company()
                if default_company:
                    vals['company_id'] = default_company.id
                else:
                    # This should never happen, but let's be safe
                    vals['company_id'] = self.env.company.id
            
            # For website_id, create a context-aware version that knows the company
            if not vals.get('website_id'):
                # Create a temporary record context with the company to get proper website
                with_company = self.with_company(vals['company_id'])
                default_website = with_company._default_website()
                if default_website:
                    vals['website_id'] = default_website.id
        
        # Call parent create
        records = super().create(vals_list)
        
        # DOUBLE CHECK: Verify and fix any records that still don't have proper values
        for record in records:
            if not record.company_id:
                record.company_id = record._default_company()
            
            if not record.website_id:
                record.website_id = record._default_website()
        
        return records
    
    def write(self, vals):
        """Override write to handle company and website changes"""
        return super().write(vals)
    
    @api.onchange('company_id')
    def _onchange_company_id(self):
        """Update website domain when company is changed in form view"""
        if self.company_id:
            # Update website domain based on new company
            return {'domain': {'website_id': [('company_id', '=', self.company_id.id)]}}
    
    @api.onchange('website_id')
    def _onchange_website_id(self):
        """Handle when website is changed in form view"""
        pass
    
    @api.constrains('company_id', 'website_id')
    def _check_company_website(self):
        """Validate website belongs to the company (company is already required)"""
        for record in self:
            # If website is set, validate it belongs to the company
            if record.website_id and record.website_id.company_id != record.company_id:
                # Try to find a website for this company
                correct_website = self.env['website'].search([
                    ('company_id', '=', record.company_id.id)
                ], limit=1)
                
                if correct_website:
                    # Use write to avoid triggering constraint recursion
                    super(MultiThemesBaseMixin, record).write({'website_id': correct_website.id})
                else:
                    super(MultiThemesBaseMixin, record).write({'website_id': False})
    
    @api.model
    def _fix_missing_company_website(self):
        """Utility method to fix records with missing company or website"""
        # Find records with missing company
        records_no_company = self.search([('company_id', '=', False)])
        if records_no_company:
            for record in records_no_company:
                record.company_id = record._default_company()
        
        # Find records with missing website (optional - only if you want to enforce website)
        records_no_website = self.search([('website_id', '=', False)])
        if records_no_website:
            for record in records_no_website:
                default_website = record._default_website()
                if default_website:
                    record.website_id = default_website
        
        return True