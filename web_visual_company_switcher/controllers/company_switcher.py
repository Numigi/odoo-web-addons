# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from odoo import http
from odoo.http import request


class CompanySwitcher(http.Controller):

    @http.route('/web/visual_company_switcher/companies', type='json', auth='user', csrf=True)
    def get_companies_data(self):
        """Return companies data formatted for OrgChart.js"""
        try:
            user = request.env.user
            allowed_companies = user.company_ids
            
            if not allowed_companies:
                return {'error': 'No companies accessible'}
            
            companies_data = []
            for company in allowed_companies:
                # Get company logo URL with proper format
                logo_url = None
                if company.logo:
                    logo_url = f'/web/image/res.company/{company.id}/logo'
                
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
            
            return {'companies': companies_data}
        except Exception as e:
            return {'error': f'Failed to load companies: {str(e)}'}

    @http.route('/web/visual_company_switcher/switch_company', type='json', auth='user', csrf=True)
    def switch_single_company(self, company_id):
        """Switch to a single company"""
        try:
            if not company_id or not isinstance(company_id, int):
                return {'error': 'Invalid company ID'}
                
            user = request.env.user
            company = request.env['res.company'].browse(company_id)
            
            if not company.exists():
                return {'error': 'Company does not exist'}
                
            if company not in user.company_ids:
                return {'error': 'Access denied to this company'}
            
            # Update user session
            request.session['allowed_company_ids'] = [company_id]
            user.with_company(company).write({'company_id': company_id})
            
            return {'success': True, 'reload': True}
        except Exception as e:
            return {'error': f'Failed to switch company: {str(e)}'}

    @http.route('/web/visual_company_switcher/switch_companies', type='json', auth='user', csrf=True)
    def switch_multiple_companies(self, company_ids):
        """Switch to multiple companies"""
        try:
            if not company_ids or not isinstance(company_ids, list):
                return {'error': 'Invalid company IDs list'}
                
            if not all(isinstance(cid, int) for cid in company_ids):
                return {'error': 'All company IDs must be integers'}
                
            user = request.env.user
            companies = request.env['res.company'].browse(company_ids)
            
            # Verify all companies exist and user has access
            for company in companies:
                if not company.exists():
                    return {'error': f'Company with ID {company.id} does not exist'}
                if company not in user.company_ids:
                    return {'error': f'Access denied to company {company.name}'}
            
            # Update user session like native Odoo behavior
            request.session['allowed_company_ids'] = company_ids
            
            # Set first company as main company only if it's different from current
            if company_ids and company_ids[0] != user.company_id.id:
                # Change main company only if needed
                first_company = request.env['res.company'].browse(company_ids[0])
                user.with_company(first_company).write({'company_id': company_ids[0]})
            
            # The key is in allowed_company_ids in session for multi-company context
            
            return {'success': True, 'reload': True}
        except Exception as e:
            return {'error': f'Failed to switch companies: {str(e)}'}