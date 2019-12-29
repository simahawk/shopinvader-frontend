# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import http, fields, _
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons.shopinvader_client.components.mixin import ProxyConsumerMixin
import logging
import werkzeug

_logger = logging.getLogger(__name__)
try:
    import addict
except ImportError:
    _logger.error('`addict` lib is required')


class BaseControllerMixin(ProxyConsumerMixin):

    context_key = ''
    context_items = addict.Dict()

    def _get_context(self, page, **kw):
        context_item = self.context_items.get(page)
        if not context_item:
            raise werkzeug.exceptions.NotFound()

        # TODO: handle requests.exceptions.ConnectionError: HTTPConnectionPool(host='odoo.master', port=8069): Max retries exceeded with url: /shopinvader/sales (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f91cd20c518>: Failed to establish a new connection: [Errno -2] Name or service not known',))

        with self.work_on_proxy() as work:
            proxy = work.component(usage='proxy')
            rest_resp = proxy.make_request(context_item.rest_endpoint, as_json=False)
        
        if request.httprequest.args.get('debug'):
            # TODO: log debug
            print("|---> Received from REST API {}".format(rest_resp))
    
        qcontext = {
            'shop_index': '/shop',
            'context_key': self.context_key,
            'context_items': self.context_items,
            'context_item': context_item,
            'context_item_data': rest_resp,
            'store_settings': self._get_store_settings(),
        }
        return context_item, qcontext

    def _render_context(self, page, **kw):
        context_item, qcontext = self._get_context(page, **kw)
        return request.render(context_item.template, qcontext)

    def _get_store_settings(self):
        return addict.Dict({
            'available_countries': request.website.invader_countries(request.lang),
        })


class AccountController(http.Controller, BaseControllerMixin):

    context_key = 'account'
    context_items = addict.Dict({
        'orders': {
            'title': _('Orders'),
            'key': 'orders',
            'handle': 'account_index',  # probably not needed
            'rest_endpoint': '/sales',
            'url': '/shop/account/orders',
            'template': 'shopinvader_frontend.account_index',
        },
        'quotations': {
            'title': _('Quotations'),
            'key': 'quotations',
            'handle': 'account_quotations',
            'rest_endpoint': '/quotations',
            'url': '/shop/account/quotations',
            'template': 'shopinvader_frontend.account_quotations',
        },
        'profile': {
            'title': _('Profile'),
            'key': 'profile',
            'handle': 'account_profile',
            'rest_endpoint': '/addresses',
            'url': '/shop/account/profile',
            'template': 'shopinvader_frontend.account_profile',
        },
        'addresses': {
            'title': _('Addresses'),
            'key': 'addresses',
            'handle': 'account_address',
            'rest_endpoint': '/addresses',
            'url': '/shop/account/addresses',
            'template': 'shopinvader_frontend.account_addresses',
        },
        'addresses_form': {
            'title': _('Address form'),
            'key': 'addresses_form',
            'handle': 'addresses_form',
            'rest_endpoint': '/addresses',
            'url': '/shop/account/addresses_form',
            'template': 'shopinvader_frontend.account_address_form',
        },
    })

    @http.route(
        ['/shop/account', '/shop/account/<page>'], type='http', auth='public', website=True, csrf=False
    )
    def account_page(self, page='orders', **kw):
        return self._render_context(page, **kw)

    def _get_context(self, page, **kw):
        context_item, qcontext = super()._get_context(page,**kw)
        context_item_data = qcontext['context_item_data']
        if context_item.rest_endpoint == '/addresses':
            addresses = context_item_data.get('data', [])
            address_by_type = {x['address_type']: x for x in addresses}
            profile_address = address_by_type.get('profile', {})

            address_by_id = {x['id']: x for x in addresses}
            address_id = int(request.params.get('item_id', '0'))
            current_address = address_by_id.get(address_id, {})
            qcontext.update({
                'profile': profile_address,
                'address': current_address,
                'addresses': [x for x in addresses if x['address_type'] != 'profile']
            })
        return context_item, qcontext


class AccountSnippetontroller(http.Controller, BaseControllerMixin):

    context_key = 'account'
    context_items = addict.Dict({
        'addresses_form': {
            'title': _('Address form'),
            'key': 'addresses_form',
            'handle': 'addresses_form',
            'rest_endpoint': '/addresses',
            'url': '/shop/account/addresses_form',
            'template': 'shopinvader_frontend.account_address_form',
        },
    })

    @http.route(
        ['/shop/account/<snippet>'], type='http', auth='public', website=True, csrf=False
    )
    def account_page(self, snippet='addresses_form', **kw):
        return self._render_context(snippet, **kw)