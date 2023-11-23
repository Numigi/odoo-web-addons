FROM quay.io/numigi/odoo-public:14.latest
MAINTAINER numigi <contact@numigi.com>

USER root
ARG GIT_TOKEN

COPY .docker_files/test-requirements.txt .
RUN pip3 install -r test-requirements.txt

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"


COPY .docker_files/test-requirements.txt .
RUN pip3 install -r test-requirements.txt

USER odoo

COPY disable_quick_create /mnt/extra-addons/disable_quick_create
COPY google_attachment /mnt/extra-addons/google_attachment
COPY web_custom_label /mnt/extra-addons/web_custom_label
COPY web_custom_modifier /mnt/extra-addons/web_custom_modifier
COPY web_editor_backend_context /mnt/extra-addons/web_editor_backend_context
COPY web_handle_condition /mnt/extra-addons/web_handle_condition
COPY web_hide_db_manager_link /mnt/extra-addons/web_hide_db_manager_link
COPY web_trash_condition /mnt/extra-addons/web_trash_condition
COPY website_google_analytics_fixed /mnt/extra-addons/website_google_analytics_fixed
COPY website_menu_by_user_status /mnt/extra-addons/website_menu_by_user_status
COPY web_search_date_range /mnt/extra-addons/web_search_date_range
COPY web_search_date_range_account /mnt/extra-addons/web_search_date_range_account
COPY website_blog_internal /mnt/extra-addons/website_blog_internal
COPY website_blog_rss_feed_disabled /mnt/website_blog_rss_feed_disabled
COPY website_landing_template /mnt/extra-addons/website_landing_template
COPY web_contextual_search_favorite /mnt/extra-addons/web_contextual_search_favorite
COPY web_list_column_width /mnt/extra-addons/web_list_column_width
COPY web_form_disable_autocomplete /mnt/extra-addons/web_form_disable_autocomplete
COPY website_login_as /mnt/extra-addons/website_login_as
COPY website_sale_wishlist_extended /mnt/extra-addons/website_sale_wishlist_extended
COPY website_slides_extended /mnt/extra-addons/website_slides_extended

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
