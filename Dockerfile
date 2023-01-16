FROM quay.io/numigi/odoo-public:14.latest
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/test-requirements.txt .
RUN pip3 install -r test-requirements.txt

USER odoo

COPY disable_quick_create /mnt/extra-addons/disable_quick_create
#COPY google_attachment /mnt/extra-addons/google_attachment
#COPY web_custom_label /mnt/extra-addons/web_custom_label
#COPY web_custom_modifier /mnt/extra-addons/web_custom_modifier
COPY web_editor_backend_context /mnt/extra-addons/web_editor_backend_context
COPY web_form_disable_autocomplete /mnt/extra-addons/web_form_disable_autocomplete
COPY web_handle_condition /mnt/extra-addons/web_handle_condition
COPY web_list_column_width /mnt/extra-addons/web_list_column_width
COPY web_trash_condition /mnt/extra-addons/web_trash_condition
#COPY web_trash_condition /mnt/extra-addons/web_trash_condition
#COPY website_google_analytics_fixed /mnt/extra-addons/website_google_analytics_fixed
COPY website_blog_internal /mnt/extra-addons/website_blog_internal
COPY website_landing_template /mnt/extra-addons/website_landing_template
COPY website_menu_by_user_status /mnt/extra-addons/website_menu_by_user_status

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
