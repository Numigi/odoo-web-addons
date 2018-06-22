# Google Attachement

This module allows to attach documents from Google Drive.

The attached documents are not stored in Odoo. Only the url and the document name are stored in Odoo.
This allows permissions to access the attached documents to be managed in Google Drive.

## Usage

* Go to any form view and click on `Attachments / From Google...`

![Sidebar](static/description/sidebar.png?raw=true)

* Authenticate to Google

![Google OAuth2](static/description/oauth2.png?raw=true)

* Select your attachments

![Google Picker](static/description/picker.png?raw=true)

## Configuration

1. Go to the [Google Developper Console](https://console.developers.google.com/apis/dashboard).
2. Setup a project with Google (if you do not have one already).
3. Create an OAuth2 Client ID.
4. Create an API Key.
5. Activate the access to the [Google Picker API](https://developers.google.com/picker/).
6. In Odoo, go to `Settings / General Settings`.
7. In the section `Attachments From Google Drive`, fill your OAuth Client ID and your API Key.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
