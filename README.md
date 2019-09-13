# Odoo Web Addons

This repository contains transversal Odoo modules related to the web user interface.

## Business Activity Agnostic

By transversal, we mean that one of these addons should be relevant for any vertical business activity.

It should not be specific to medical, insurances, tourism, construction, etc.

## Application Agnostic

It also should not add fields that will be used in some application more than another.

For example, it should not add a field that is related to accounting, sales, inventory or purchases.

## Model Agnostic

These modules are not related to a specific model more than another.

For modules related to partners, see [partner-addons](https://github.com/Numigi/odoo-partner-addons).
For modules related to products, see [product-addons](https://github.com/Numigi/odoo-product-addons).

## Related to User Interface

If a transversal Odoo module is not related to user interface, it could be placed in [base-addons](https://github.com/Numigi/base-addons).

There is a main reason for seperating web interface modules from other transversal modules.
Web interface modules usually require integration tests (either manual or automated).
In contrast, other transversal modules are usually easily covered with Python tests.
The maintenance effort is therefore higher with web interface modules.
