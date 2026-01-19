=========================
Web Attachment Size Limit
=========================

This module allows you to set a global limit on the size of files that can be uploaded to Odoo.

It overrides the standard upload controller to verify the file size server-side, preventing users from uploading files larger than the configured limit.

Configuration
=============

To configure the maximum upload size:

1.  Go to **Settings > Technical > Parameters > System Parameters**.
2.  Search for the key ``web.max_file_upload_size``.
3.  Set the value in **bytes**.

    * Example for 10 MB: ``10485760``
    * Example for 5 MB: ``5242880``
    * Calculation: ``Size in MB * 1024 * 1024``

**Note:**
If the parameter does not exist, the module creates it automatically upon installation with a default value of 10 MB.

Usage
=====

When a user tries to upload a file (e.g., in the chatter, documents, or binary fields) that exceeds the configured limit, the upload is blocked, and an error message is displayed:

    "File too large. Global limit is X MB."

Contributors
------------

The `Numigi <https://numigi.com/r/home>`_ team is the contributor to this project. We help Quebec companies implement Odoo and Konvergo ERP.