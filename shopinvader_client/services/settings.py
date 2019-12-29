# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=method-required-super, consider-merging-classes-inherited

import json

# from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component


class SettingsService(Component):
    _name = "shopinvader.settings.service"
    _inherit = "base.shopinvader.service"
    _usage = "settings"
    _expose_model = "website"

    # The following method are 'public' and can be called from the controller.

    def update(self, **params):
        settings = self.website.update_invader_settings(
            self._prepare_update_params(params)
        )
        return json.dumps(settings)

    def _validator_update(self):
        # TODO: better validation?
        return {
            "all_filters": {"type": "dict", },
            "available_countries": {"type": "dict", },
            "currencies_rate": {"type": "dict", },
        }

    def _prepare_update_params(self, params):
        return params
