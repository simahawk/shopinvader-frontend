# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import http
from odoo.http import request
from odoo.addons.shopinvader_client.components.mixin import ProxyConsumerMixin

import logging

_logger = logging.getLogger(__name__)

try:
    import addict
except ImportError:
    _logger.error('`addict` lib is required')


class ProductController(http.Controller, ProxyConsumerMixin):

    template = 'shopinvader_frontend.product_page'

    @http.route(
        '/shop/product/<url_key>', type='http', auth='public', website=True
    )
    def product_page(self, url_key, ref=None, **kwargs):
        search_form = {
            'domain': [('url_key', '=', url_key)],
        }
        # TODO: this requires `shopinvader_rest_product` to be installed on master.
        # We should make this point pluggable to be replaceable with search engine lookup.
        # We could delegate product retrieval to a specific proxy component for product lookup.
        with self.work_on_proxy(form=search_form) as work:
            proxy = work.component(usage='proxy')
            response = proxy.make_request('/product/search', as_json=False)

        variants = response.get('data', [])
        if not variants:
            # TODO: redirect to a nicer page when a product is not found
            return request.not_found()

        product_variant = variants[0]
        if ref:
            # we got a specific variant demand
            # `ref` name comes from liquid templates, just keep it for now
            specific_variant = [x for x in variants if x['sku'] == ref]
            if specific_variant:
                product_variant = specific_variant[0]

        if 'price' in product_variant:
            # in locomotive they have the concept of "role" per user
            # by default is "default" and they can have a price per role
            # based on the pricelist for instance.
            # See shopinvader.variant._get_all_price.
            product_variant['price'] = product_variant['price']['default']
        
        product_category = {}
        if product_variant.get('categories', []):
            # get last
            product_category = product_variant.get('categories')[-1]
        qcontext = {
            'all_variants': variants,
            'product_variant': product_variant,
            'product_category': product_category,
        }
        return request.render(self.template, qcontext)
