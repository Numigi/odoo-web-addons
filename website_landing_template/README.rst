Website Landing Page
====================

.. contents:: Table of Contents

Context
-------
In vanilla Odoo, when you create a website page, it comes with the default
header and footer, including the main menu.

.. image:: website_landing_template/static/description/vanilla_odoo_page.png

However, you might sometimes need to create a website page without those elements.
This is what we call here a ``Landing Page``.

Overview
--------
This module adds a website page that can be used to create landing pages.

.. image:: website_landing_template/static/description/template_page.png

When selecting this template, the original header and footer are absent from the page.

.. image:: website_landing_template/static/description/new_page.png

Known Issues
------------
The implementation of landing pages is purely aesthetic.
If you open the sources of the page, you will see that the header and footer are still present.
They are only hidden using css.

The reason is that completely removing these elements could have side effects related to the javascript framework.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
