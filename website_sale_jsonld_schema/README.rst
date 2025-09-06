Website Sale JSON-LD Schema
===========================
This module adds a complete and dynamic JSON-LD schema.org script to product pages for Google Merchant Center and Rich Results optimization.

The module injects structured data in JSON-LD format into Odoo eCommerce product pages, providing search engines with detailed product information including brand, GTIN, MPN, pricing, availability, and images.

.. contents:: Table of Contents

Context
-------
Modern e-commerce websites require structured data to improve SEO performance and enable rich search results. Google Merchant Center and other search engines rely on schema.org markup to understand product information and display enhanced search results.

Vanilla Odoo does not provide structured data markup for product pages, missing opportunities for:

* Rich search results with product images, prices, and availability
* Better Google Shopping integration
* Improved SEO rankings
* Enhanced click-through rates from search results

Overview
--------
This module automatically generates schema.org Product structured data in JSON-LD format for each product page. The structured data includes:

* **Product Information**: Name, description, SKU
* **Brand Information**: Product brand (requires product_brand module)
* **Category**: Product type from first public category in breadcrumb format
* **Google Category**: Google Product Category taxonomy mapping
* **Identifiers**: GTIN from UPC barcode, MPN when available
* **Pricing**: Current price with proper currency and pricelist support
* **Images**: Main product image and additional gallery images with fallback
* **Shipping**: Weight information when available
* **Availability**: Always set to "InStock"
* **Condition**: Always set to "NewCondition"
* **Geographic Scope**: Company country when configured

Features
--------

Multi-language Support
**********************
The module automatically adapts content to the current website language, ensuring localized product names and descriptions appear in the structured data.

Multi-currency Support
**********************
Pricing information uses the current website pricelist and currency, making the module suitable for international e-commerce sites.

Robust Image Handling
*********************
* Uses main product image and additional gallery images
* Automatic fallback to placeholder image when no images are available  
* Prevents JSON syntax errors from empty image arrays

Safe JSON Generation
********************
All text content is properly escaped to prevent JSON syntax errors from special characters like quotes and backslashes in product names or descriptions.

Configuration
-------------
The module works automatically once installed. No additional configuration is required.

**Dependencies**: Ensure the following modules are installed:
* `website_sale` (Odoo core)
* `product_barcode_upc` (for GTIN/UPC support)
* `product_brand` (OCA module for brand information)

**Google Product Categories Setup**:

1. Go to **Website > Products > eCommerce Categories**
2. Edit each category and fill the **Google Product Category** field
3. Use the complete Google taxonomy path (e.g., "Santé et beauté > Équipement médical > Mannequin d'enseignement médical")
4. All products in that category will automatically inherit this Google category in their JSON-LD

Technical Notes
---------------

Availability and Condition
***************************
The structured data always shows:

* **Availability**: "InStock" - Products are always marked as available regardless of stock levels
* **Condition**: "NewCondition" - All products are marked as new condition

This design choice ensures consistent search engine optimization while avoiding complex inventory tracking in structured data.

JSON-LD Location
****************
The structured data script is injected inside the `<div id="wrap">` element of product pages, ensuring proper page integration without interfering with existing functionality.

Data Sources
************
* **GTIN**: Uses UPC barcode field from `product_barcode_upc` module
* **MPN**: Falls back to manufacturer part number when UPC is not available
* **Brand**: Uses brand information from `product_brand` module
* **Category**: Uses first public category (`public_categ_ids`) with breadcrumb format (e.g., "Squelettes > Accessoires")
* **Google Category**: Uses `google_product_category` field from the first public category
* **Pricing**: Respects current pricelist and currency context
* **Images**: Includes main image and additional product template images

Contributors
------------

The `Numigi <https://numigi.com/r/home>`_ team is the contributor to this project. We help Quebec companies implement Odoo and Konvergo ERP.