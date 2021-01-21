FROM quay.io/numigi/odoo-public:12.latest
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/test-requirements.txt .
RUN pip3 install -r test-requirements.txt

USER odoo

COPY disable_quick_create /mnt/extra-addons/disable_quick_create
COPY google_attachment /mnt/extra-addons/google_attachment
COPY web_contextual_search_favorite /mnt/extra-addons/web_contextual_search_favorite
COPY web_custom_label /mnt/extra-addons/web_custom_label
COPY web_custom_modifier /mnt/extra-addons/web_custom_modifier
COPY web_editor_backend_context /mnt/extra-addons/web_editor_backend_context
COPY web_form_disable_autocomplete /mnt/extra-addons/web_form_disable_autocomplete
COPY web_handle_condition /mnt/extra-addons/web_handle_condition
COPY web_list_column_width /mnt/extra-addons/web_list_column_width
COPY web_search_date_range /mnt/extra-addons/web_search_date_range
COPY web_search_date_range_account /mnt/extra-addons/web_search_date_range_account
COPY web_trash_condition /mnt/extra-addons/web_trash_condition
COPY website_menu_by_user_status /mnt/extra-addons/website_menu_by_user_status

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
