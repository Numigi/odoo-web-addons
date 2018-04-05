FROM quay.io/numigi/odoo-public:11.0
MAINTAINER numigi <contact@numigi.com>

COPY disable_quick_create /mnt/extra-addons/disable_quick_create
COPY ui_color_red /mnt/extra-addons/ui_color_red
COPY web_list_column_width /mnt/extra-addons/web_list_column_width

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
