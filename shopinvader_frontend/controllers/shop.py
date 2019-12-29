# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import http
from odoo.http import request


class ShopHomeController(http.Controller):

    template = 'shopinvader_frontend.shop_home'

    @http.route(
        '/shop', type='http', auth='public', website=True
    )
    def shop_home(self, **kw):
        return request.render(self.template, {})
