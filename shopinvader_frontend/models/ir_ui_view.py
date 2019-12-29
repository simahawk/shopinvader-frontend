# -*- coding: utf-8 -*-
# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models
from odoo.http import request


class IrUiView(models.Model):
    _inherit = ["ir.ui.view"]

    @api.model
    def _prepare_qcontext(self):
        qcontext = super(IrUiView, self)._prepare_qcontext()
        block_settings = {'display_add_to_cart': True}
        qcontext['product'] = 'qrcontext product'
        qcontext['block_settings'] = block_settings
        qcontext['url_base'] = '/shop'
        qcontext['currency'] = 'CHF'
        # Used in the quantity selector snippet !?
        qcontext['small'] = False
        qcontext['product_url'] = self.make_product_url
        return qcontext

    def make_product_url(self, product, added_to_cart=False):
        url = '/shop/product/' + product['url_key']
        if added_to_cart:
            url += '?addtocart_product_id={}'.format(product['objectID'])
        return url

