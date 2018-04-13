FROM quay.io/numigi/odoo-public:10.0
MAINTAINER numigi <contact@numigi.com>

USER root

# Variable used for fetching private git repositories.
ARG GIT_TOKEN

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install_all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY disable_quick_create /mnt/extra-addons/disable_quick_create
COPY ui_color_blue /mnt/extra-addons/ui_color_blue
COPY ui_color_gray /mnt/extra-addons/ui_color_gray
COPY ui_color_orange /mnt/extra-addons/ui_color_orange
COPY ui_color_red /mnt/extra-addons/ui_color_red

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
