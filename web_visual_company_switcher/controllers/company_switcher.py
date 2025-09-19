# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
import base64
from odoo import http
from odoo.http import request


class CompanySwitcher(http.Controller):

    @http.route('/web/visual_company_switcher/companies', type='json', auth='user', csrf=True)
    def get_companies_data(self):
        """Return companies data with correct current/allowed status"""
        try:
            user = request.env.user
            available_companies = user.company_ids
            
            if not available_companies:
                return {'error': 'No companies accessible'}
            
            # Get current session info
            current_company_id = user.company_id.id
            session_allowed_ids = request.session.get('allowed_company_ids', [current_company_id])
            
            
            companies_data = []
            for company in available_companies:
                # Get company logo as base64
                logo_base64 = None
                if company.logo:
                    logo_base64 = company.logo.decode('utf-8') if isinstance(company.logo, bytes) else company.logo
                
                # Force int conversion for comparison
                company_id_int = int(company.id)
                current_company_id_int = int(current_company_id)
                session_allowed_ints = [int(x) for x in session_allowed_ids]
                
                is_current = company_id_int == current_company_id_int
                is_allowed = company_id_int in session_allowed_ints
                
                company_data = {
                    'id': company_id_int,  # Ensure int type
                    'name': company.name,
                    'title': company.display_name,
                    'parent_id': company.parent_id.id if company.parent_id else None,
                    'logo': logo_base64,
                    'current': is_current,
                    'allowed': is_allowed
                }
                companies_data.append(company_data)
            
            result = {
                'companies': companies_data,
                'current_allowed_companies': [int(x) for x in session_allowed_ids],  # Ensure int list
                'current_company_id': int(current_company_id)  # Ensure int
            }
            
            return result
            
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
        """Switch to multiple companies - mimics native Odoo multi-company behavior"""
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
            
            # This is the key: set allowed_company_ids in session to enable multi-company context
            # This mimics exactly what Odoo's native company switcher does
            request.session['allowed_company_ids'] = company_ids
            
            # Set first company as main company (like native behavior)
            if company_ids:
                main_company_id = company_ids[0]
                if main_company_id != user.company_id.id:
                    # Update user's main company
                    main_company = request.env['res.company'].browse(main_company_id)
                    user.with_company(main_company).write({'company_id': main_company_id})
            
            # Return companies info for frontend update
            companies_info = []
            for company in companies:
                companies_info.append({
                    'id': company.id,
                    'name': company.name,
                    'is_main': company.id == company_ids[0]
                })
            
            return {
                'success': True, 
                'reload': True,
                'companies': companies_info,
                'main_company_id': company_ids[0] if company_ids else None
            }
        except Exception as e:
            return {'error': f'Failed to switch companies: {str(e)}'}