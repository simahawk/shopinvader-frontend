# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import http
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons.shopinvader_client.components.mixin import ProxyConsumerMixin

from collections import namedtuple

CART_INDEX =  {
    'key': 'cart_index',
    'name': 'index',
    'url': '/shop/cart',
    'endpoint': '/cart',
    'extra_endpoints': [],
    'next_step_key': 'cart_address',
}
CART_SHIPPING = {
    'key': 'cart_address',
    'name': 'address',
    'url': '/shop/cart/address',
    'endpoint': '/cart',
    'extra_endpoints': [
        # endpoint, response key, destination key
        ('/addresses', 'data', 'addresses')
    ],
    'next_step_key': 'cart_checkout',
}
CART_CHECKOUT = {
    'key': 'cart_checkout',
    'name': 'checkout',
    'url': '/shop/cart/checkout',
    'endpoint': '/cart',
    'extra_endpoints': [],
    'next_step_key': 'cart_checkout',
}
_CART_STEPS = {
    'cart_index': CART_INDEX,
    'cart_address': CART_SHIPPING,
    'cart_checkout': CART_CHECKOUT,
}

CartStep = namedtuple(
    'CartStep',
    'key name url endpoint extra_endpoints next_step_key next_step'
)
CartStep.__new__.__defaults__ = (None, ) * len(CartStep._fields)

CART_STEPS = {}

for key, data in _CART_STEPS.items():
    if data['next_step_key'] and _CART_STEPS.get(data['next_step_key']):
        data['next_step'] = CartStep(**_CART_STEPS.get(data['next_step_key']))
    CART_STEPS[key] = CartStep(**data)

# for name, step in CART_STEPS.items():
#     step.next_step  = CART_STEPS.get(step.next_step_key)


class CartController(http.Controller, ProxyConsumerMixin):

    template_prefix = 'shopinvader_frontend.'
    # Probably given by Odoo main !?
    cart_steps = CART_STEPS

    @http.route(['/shop/cart', '/shop/cart/<step_key>'], type='http', auth='public', website=True)
    def cart_page(self, step_key='cart_index', **kwargs):
        """Display the cart content."""
        if not step_key.startswith('cart_'):
            # TODO: discrepancy between cart step key and url 
            # + steps config on odoo master forces to have such tricks.
            # Eg: address -> cart_address
            step_key = 'cart_' + step_key
        step = self.cart_steps.get(step_key)
        if not step:
            return request.not_found()

        if step.key != 'cart_index' and not request.session.uid:
            return http.redirect_with_hash('/web/login?redirect={}'.format(step.url))

        with self.work_on_proxy() as work:
            proxy = work.component(usage='proxy')
            response = proxy.make_request(step.endpoint, as_json=False)

        store = response.get('store_cache', {})
        store['available_countries'] = request.website.invader_countries(request.lang)

        # call additional endpoints
        extra_endpoints = step.extra_endpoints or []
        for extra_endpoint, response_key, destination_key in extra_endpoints:
            with self.work_on_proxy() as work:
                proxy = work.component(usage='proxy')
                response = proxy.make_request(extra_endpoint, as_json=False)
                store[destination_key] = response[response_key]

        qcontext = {
            'store': store,
            'cart': store.get('cart', {}),
            'cart_step': step,
            'all_cart_steps': self.cart_steps,
        }
        return request.render(self.template_prefix + step.key, qcontext)
