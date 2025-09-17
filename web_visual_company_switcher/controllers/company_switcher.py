# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from odoo import http
from odoo.http import request


class CompanySwitcher(http.Controller):

    @http.route('/web/visual_company_switcher/companies', type='json', auth='user')
    def get_companies_data(self):
        """Return companies data formatted for OrgChart.js"""
        user = request.env.user
        allowed_companies = user.company_ids
        
        companies_data = []
        for company in allowed_companies:
            # Get company logo URL
            logo_url = '/web/image/res.company/%d/logo' % company.id if company.logo else None
            
            company_data = {
                'id': company.id,
                'name': company.name,
                'title': company.display_name,
                'parent_id': company.parent_id.id if company.parent_id else None,
                'logo': logo_url,
                'current': company.id == user.company_id.id,
                'allowed': True
            }
            companies_data.append(company_data)
        
        return companies_data

    @http.route('/web/visual_company_switcher/switch_company', type='json', auth='user')
    def switch_single_company(self, company_id):
        """Switch to a single company"""
        user = request.env.user
        company = request.env['res.company'].browse(company_id)
        
        if company not in user.company_ids:
            return {'error': 'Access denied to this company'}
        
        # Update user session
        request.session['allowed_company_ids'] = [company_id]
        user.with_context(force_company=company_id).write({'company_id': company_id})
        
        return {'reload': True}

    @http.route('/web/visual_company_switcher/switch_companies', type='json', auth='user')
    def switch_multiple_companies(self, company_ids):
        """Switch to multiple companies"""
        user = request.env.user
        companies = request.env['res.company'].browse(company_ids)
        
        # Verify access to all companies
        for company in companies:
            if company not in user.company_ids:
                return {'error': f'Access denied to company {company.name}'}
        
        # Update user session
        request.session['allowed_company_ids'] = company_ids
        # Set first company as active
        if company_ids:
            user.with_context(force_company=company_ids[0]).write({'company_id': company_ids[0]})
        
        return {'reload': True}