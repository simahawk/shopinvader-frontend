from odoo import _
from odoo.addons.component.core import AbstractComponent
from odoo.exceptions import MissingError
from odoo.osv import expression


class BaseShopinvaderService(AbstractComponent):
    _name = "base.shopinvader.service"
    _inherit = "base.rest.service"
    _collection = "shopinvader.client"
    _expose_model = None

    @property
    def website(self):
        return self.work.website

    def _get(self, _id):
        domain = expression.normalize_domain(self._get_base_search_domain())
        domain = expression.AND([domain, [("id", "=", _id)]])
        record = self.env[self._expose_model].search(domain)
        if not record:
            raise MissingError(
                _("The record %s %s does not exist")
                % (self._expose_model, _id)
            )
        else:
            return record

    def _get_base_search_domain(self):
        return []

    def _get_openapi_default_parameters(self):
        defaults = super(
            BaseShopinvaderService, self
        )._get_openapi_default_parameters()
        defaults.append(
            {
                "name": "API-KEY",
                "in": "header",
                "description": "Auth API key",
                "required": True,
                "schema": {"type": "string"},
                "style": "simple",
            }
        )
        return defaults
