# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

import werkzeug
from odoo.addons.base_rest.controllers import main
from odoo.exceptions import MissingError
from odoo.http import request

_logger = logging.getLogger(__name__)


class OdooClientRestController(main.RestController):
    """REST endpoints for odoo.master sync.

    Master Odoo will call these services to update settings and other information
    on Odoo client.
    """

    _root_path = "/shopinvader/"
    _collection_name = "shopinvader.client"
    _default_auth = "api_key"

    @classmethod
    def _get_website(cls, current_request):
        return request.env["website"]._get_from_http_request(current_request)

    def _get_component_context(self):
        res = super()._get_component_context()
        res["website"] = self._get_website(request)
        return res
