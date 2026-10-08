Website Sale Carrier Account
============================
This module allows customers to enter their own carrier account number during the eCommerce checkout.

When a delivery carrier is configured to request a carrier account number, a field is displayed at the delivery step of the checkout. The number entered by the customer is stored on the sale order and appended to the order notes.

Configuration
-------------
On a delivery method (``Inventory > Configuration > Delivery Methods``), check the field **Carrier Account Number Required** to allow customers to enter their carrier account number for that carrier.

Usage
-----
At the delivery step of the checkout, when the customer selects a carrier that requires a carrier account number, an input field is displayed.

The carrier account number entered by the customer is:

* stored on the sale order in the **Carrier Account Number** field;
* appended to the sale order notes;
* logged in the order chatter.

Contributors
------------

The `Numigi <https://numigi.com/r/home>`_ team is the contributor to this project. We help Quebec companies implement Odoo and Konvergo ERP.