Web Custom Modifier
===================
This module allows to customize modifiers on form view nodes.

For example, it allows to make a field readonly, invisible or required.

Usage
-----
As system administrator, I go to `Settings / Technical / User Interface / Custom Modifiers`.

.. image:: static/description/custom_modifier_menu.png

I create a new custom modifier.

.. image:: static/description/new_custom_modifier.png

The modifier is configured to make the field ``default_code`` of a product required.

After refreshing my screen, I go to the form view of a product.

I notice that the field ``default_code`` is required.

.. image:: static/description/product_form.png

Advanced Usage
--------------
In the field ``Type``, I can select ``Xpath``.
This allows to set a modifier for a specific view node, such as a button.

.. image:: static/description/button_modifier.png

The example above hides the a button in the form view of a product.

Hide Selection Item
-------------------
Since version ``1.1.0``, the module allows to hide an item (option) of a selection field.

.. image:: static/description/hide_selection_item_modifier.png

The above example hides the type of address ``Other``.

.. image:: static/description/contact_form_without_selection_item.png

Beware that if the hidden option is already selected on a record,
it will look as it was never set.

.. image:: static/description/contact_form_type_not_selected.png

Therefore, this feature should only be used to hide options that are never used.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
