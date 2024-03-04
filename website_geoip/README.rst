Website GeoIP
=============

.. contents:: Table of Contents

Context
=======

Odoo offers to manage the GeoIP using a GeoLite2-City.mmdb file. The assignment of the IP to the user session is already provided in the OpenObjec ORM

This module adds the visitor website GeoIP datas as a session variable :

https://www.odoo.com/documentation/14.0/fr/applications/websites/website/configuration/on-premise_geo-ip-installation.html

This method requires periodic updating of the .mmdb file. Each time you have to fetch the latest update, put it in the right location and then give it the right system permissions so that it is recognized by odoo.

Overview
========
Instead of using the GeoLite2-City.mmd data file and maintaining it, we use a web service API. The latter provides the data that we will format firstly, then assign them to the session variable “geoip” in a second step

Usage
=====

Get the Vistor's IP
-------------------

``ip_address = request.httprequest.environ['REMOTE_ADDR']``

Request the webservice
----------------------

``urlData = "https://get.geojs.io/v1/ip/country/%s.json" % ip_address``
``webURL = urllib.request.urlopen(urlData)``
``data = webURL.read()``
``encoding = webURL.info().get_content_charset('utf-8')``
``res = json.loads(data.decode(encoding))``

Data formatting
---------------

``geoip = {``
        ``'city': res['name'] if 'name' in res.keys() else '',``
        ``'country_code': res['country'] if 'country' in res.keys() else '',``
        ``'country_name': res['name'] if 'name' in res.keys() else '',``
        ``'region': res['name'] if 'name' in res.keys() else '',``
        ``'time_zone': res['country'] if 'country' in res.keys() else '',``
        ``}``

Geop session variable definition:
---------------------------------

``request.session['geoip'] = geoip``

Basic Use
---------
In any page or part of the website you can call the geoip session variable using :

request.session.get('geoip')

for example:

``<h1 class="text-center" t-esc="request.session.get('geoip')"/>"``

or

``<t t-set="country" t-value="request.session.get('geoip')"/>``
``<t t-if="country['country_code'] == 'CA'">``



``code html/qweb/xml``

``</t>``

Attention : if you set t-if tags inside the oe_structure div , it will break the snippets drag-and-drop zone of the website builder.


Sample of Conditional snippets
------------------------------
``<!--Start -->``
``<t t-name="website.pagename">``
  ``<t t-call="website.layout">``
    ``<!-- ZONE 1 -->``
    ``<!-- Div snippet start -->``
    ``<div id="wrap" class="oe_structure oe_empty">``

      ``<!-- On peut déposer des snippets ici -->``
      ``<section data-snippet="s_snippet" data-name="Snippet">``
        ``Snippet without condition``
      ``</section>``

    ``</div>``
    ``<!-- Div snippet end -->``


    ``<!-- conditional section start -->``
    ``<t t-set="country" t-value="request.session.get('geoip')" />``

    ``<div class="oe_structure oe_empty">``

     ``<!--  Canada bloc -->``
      ``<t t-if="country['country_code'] == 'CA'">``
        ``<!-- CA content -->``
      ``</t>``

      ``<!-- France bloc -->``
      ``<t t-elif="country['country_code'] == 'FR'">``
        ``<!--France content -->``
      ``</t>``

    ``</div>``
    ``<!-- conditional section end  -->``

    ``<!-- ZONE 2 -->``
   ``<!-- Start of a new structure for depositing snippets not conditional on GeoIP -->``
   ``<div class="oe_structure oe_empty">``

       ``<!-- Here you can submit the extracts -->``

   ``</div>``
    ``<!-- Closing the unconditional snippet structure -->``

  ``</t>``
``</t>``


Contributors
============
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
================
* Meet us at https://bit.ly/numigi-com
