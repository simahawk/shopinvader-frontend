# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import http
from odoo.http import request
from ..components.mixin import ProxyConsumerMixin


class ProxyController(http.Controller, ProxyConsumerMixin):
    """Proxy invader calls to Master Odoo."""

    # TODO: handle CSRF
    @http.route(
        '/invader/<path:endpoint>',
        type='http',
        auth='public',
        csrf=False,
        website=True,
    )
    def proxy_invader_endpoint(self, endpoint, **kwargs):
        with self.work_on_proxy() as work:
            proxy = work.component(usage='proxy')
            result = proxy.make_request(endpoint)
            return result
