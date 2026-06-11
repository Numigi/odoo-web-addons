FROM quay.io/numigi/odoo-public:18.latest
LABEL maintainer="contact@numigi.com"

USER root

COPY .docker_files/test-requirements.txt .
RUN pip3 install -r test-requirements.txt

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"


COPY .docker_files/test-requirements.txt .
RUN pip3 install -r test-requirements.txt

USER odoo

COPY web_custom_label /mnt/extra-addons/web_custom_label
COPY web_custom_modifier /mnt/extra-addons/web_custom_modifier
COPY web_db_name_display /mnt/extra-addons/web_db_name_display

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
