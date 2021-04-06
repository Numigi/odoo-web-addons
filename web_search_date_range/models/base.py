# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class Base(models.AbstractModel):

    _inherit = 'base'

    @api.model
    def _where_calc(self, domain, active_test=True):
        domain = _convert_domain(self.env, domain)
        return super()._where_calc(domain, active_test)


def _convert_domain(env, domain):
    if not isinstance(domain, list):
        return domain

    return list(_iter_leaves(env, domain))


def _iter_leaves(env, domain):
    for leaf in domain:
        if _is_date_range(leaf):
            for range_leaf in _to_date_range(env, leaf):
                yield range_leaf
        else:
            yield leaf


def _is_date_range(leaf):
    return (
        isinstance(leaf, (list, tuple))
        and len(leaf) == 3
        and leaf[1] == "range"
    )


def _to_date_range(env, leaf):
    field_name = leaf[0]
    range_id = leaf[2]
    range_ = env["search.date.range"].browse(range_id)
    return range_.generate_domain(field_name)
