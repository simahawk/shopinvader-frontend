# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import http
from odoo.http import request
from odoo.addons.shopinvader_client.components.mixin import ProxyConsumerMixin


class ProductController(http.Controller, ProxyConsumerMixin):

    template = 'shopinvader_frontend.category_page'

    @http.route(
        '/shop/category/<url_key>', type='http', auth='public', website=True
    )
    def category_page(self, url_key, ref=None, **kwargs):
        search_form = {
            'domain': [('url_key', '=', url_key)],
        }
        # TODO: this requires `shopinvader_rest_product` to be installed on master.
        # We should make this point pluggable to be replaceable with search engine lookup.
        # We could delegate product retrieval to a specific proxy component for product lookup.
        with self.work_on_proxy(form=search_form) as work:
            proxy = work.component(usage='proxy')
            response = proxy.make_request('/category/search', as_json=False)

        category = response.get('data', [])
        if not category:
            # TODO: redirect to a nicer page when a product is not found
            return request.not_found()

        category = category[0]

        search_form = {
            'domain': [('category_id', '=', category['objectID'])],
        }
        # NOTE: we are doing to REST  calls but it could be just one w/ a specific endpoint.
        # ATM  we don't care, sorry :)
        with self.work_on_proxy(form=search_form) as work:
            proxy = work.component(usage='proxy')
            response = proxy.make_request('/product/search', as_json=False)
        
        variants = response.get('data', [])
        qcontext = {
            'product_category': category,
            'products': variants,
        }
        return request.render(self.template, qcontext)

