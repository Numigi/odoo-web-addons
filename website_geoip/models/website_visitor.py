# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from datetime import datetime
from odoo import fields, models, api, _
from odoo.http import request
import logging
import json
import urllib.request


class WebsiteVisitor(models.Model):

    _inherit = 'website.visitor'

    geoip = fields.Char('GeoIP')

    def _handle_website_page_visit(self, website_page, visitor_sudo):
        """ Called on dispatch. This will create a website.visitor if the http request object
        is a tracked website page or a tracked view. Only on tracked elements to avoid having
        too much operations done on every page or other http requests.
        Note: The side effect is that the last_connection_datetime is updated ONLY on tracked elements."""
        ip_address = request.httprequest.environ['REMOTE_ADDR']
        if ip_address:
            urlData = "http://ip-api.com/json/%s" % ip_address
            webURL = urllib.request.urlopen(urlData)
            data = webURL.read()
            encoding = webURL.info().get_content_charset('utf-8')
            res = json.loads(data.decode(encoding))
            geoip = {
                      'city': res['city'] if 'city' in res.keys() else '',
                      'country_code': res['countryCode'] if 'countryCode' in res.keys() else '',
                      'country_name': res['country'] if 'country' in res.keys() else '',
                      'region': res['regionName'] if 'regionName' in res.keys() else '',
                      'time_zone': res['timezone'] if 'timezone' in res.keys() else '',

            }
        else:
            geoip = {
                'country_code': 'CA',
                'country_name': 'Canada',
            }
        request.session['geoip'] = geoip
        if visitor_sudo.geoip != geoip['country_code']:
            visitor_sudo.write({'geoip': geoip['country_code']})

        url = request.httprequest.url
        website_track_values = {
            'url': url,
            'visit_datetime': datetime.now(),
        }
        if website_page:
            website_track_values['page_id'] = website_page.id
            domain = [('page_id', '=', website_page.id)]
        else:
            domain = [('url', '=', url)]
        visitor_sudo._add_tracking(domain, website_track_values)
        if visitor_sudo.lang_id.id != request.lang.id:
            visitor_sudo.write({'lang_id': request.lang.id})

