# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import json
import logging
import os
import re

import requests
import werkzeug
from werkzeug.datastructures import ImmutableOrderedMultiDict

from odoo.addons.component.core import AbstractComponent, Component

_logger = logging.getLogger(__name__)

API_KEY = 'secret_flying_saucer'
BACKEND_URL = 'http://odoo.master:8069'

# TODO: check
# https://github.com/shopinvader/locomotive-shopinvader/blob/984262e9e09a38f06e8c35c4dd106d57c77966cf/lib/shop_invader/services/erp_service.rb


class BaseShopinvaderProxy(AbstractComponent):
    _name = "base.shopinvader.proxy"

    @property
    def request(self):
        return self.work.request

    @property
    def form(self):
        return self.work.form

    @property
    def website(self):
        return self.work.request.website

    @property
    def user(self):
        return self.work.user

    @property
    def customer_email(self):
        if not self.user:
            return ''
        email = self.user.partner_id.email
        if os.getenv('INVADER_FAKE_CUSTOMER'):
            email = os.getenv('INVADER_FAKE_CUSTOMER')
            _logger.info('Using INVADER_FAKE_CUSTOMER=%s', email)
        return email

    def anonymous(self):
        return not self.request.session.uid

    def _get_api_key(self):
        return self.website.shopinvader_master_api_key or API_KEY  # FIXME

    def _get_odoo_backend_url(self):
        return self.website.shopinvader_master_url or BACKEND_URL  # FIXME

    def _make_url(self, endpoint, prefix):
        return '/'.join(
            [
                self._get_odoo_backend_url().rstrip('/'),
                prefix.strip('/'),
                endpoint.lstrip('/'),
            ]
        )

    def _make_headers(self):
        _headers = {
            'API_KEY': self._get_api_key(),
            'SESS_CART_ID': str(self.request.session.get('cart_id', 0)),
        }
        if self.customer_email:
            _headers['PARTNER_EMAIL'] = self.customer_email
        return _headers


class Proxier(Component):

    _name = 'shopinvader.client.proxy'
    _inherit = "base.shopinvader.proxy"
    _usage = 'proxy'

    REQUEST_TIMEOUT = 10

    def _convert_str2dict(self, dict_repr, value):
        """Transorm a string representing dictionnary assignation into a dict.

            For a `dict_repr` formatted like this
                foo[one][two]

            This dict would be returned

                {'foo': {'one': {'two': value}}}

            Note : could be updated to use
            https://github.com/OCA/website-cms/blob/5a5bf1c5a8d4641638d5d98c87238b98f99ecb77/cms_form/marshallers.py#L66

        """
        keys = [
            item for item in re.findall(r'[^\[\]]*', dict_repr) if item != ''
        ]
        keys = keys[::-1]
        res = {keys.pop(0): value}
        for item in keys:
            res = {item: res}
        return res

    # TODO: check all the subtles here
    # https://github.com/shopinvader/locomotive-shopinvader
    # /blob/v4.0.x/lib/shop_invader/middlewares/erp_proxy.rb
    def _make_request(self, endpoint, prefix='/shopinvader', method=''):
        # TODO: shall we use a persistent connection w/ specific session?
        # Note : I do think that only GET are done from here all POST are
        #        done from the browser directely (@TDu: ????)
        method = method or self.request.httprequest.method
        url = self._make_url(endpoint, prefix)
        headers = self._make_headers()
        payload = self.form
        if isinstance(self.form, ImmutableOrderedMultiDict):
            payload = self.form.to_dict()

        # Those should not be sent to the rest api but kept when the repsonse arrived
        payload.pop('invader_error_url', '')
        payload.pop('invader_success_url', '')

        updated_payload = {}
        for key, value in payload.items():
            if '[' in key:
                o = self._convert_str2dict(key, value)
                updated_payload.update(o)
            else:
                updated_payload[key] = value
        kwargs = {}
        kwargs['json'] = updated_payload
        return requests.request(
            method,
            url,
            headers=headers,
            timeout=self.REQUEST_TIMEOUT,
            **kwargs
        )

    def make_request(self, endpoint, as_json=True, method=''):
        response = self._make_request(endpoint, method=method)
        data = {}
        got_json = response.headers["content-type"] == "application/json"
        # TODO:: handle form errors properly  (requires improvement in base_rest likely)
        # (Pdb++) response.json()
        # {'name': 'Bad Request', 'description': "<p>BadRequest {'phone': ['empty values not allowed']}</p>", 'code': 400}
        # See https://github.com/OCA/rest-framework/issues/42
        if response.status_code == 200 and got_json:
            data = response.json()
            self._prepare_result(response, data)
        if self._need_forced_redirection(data):
            return self._handle_redirection(response, data)
        if got_json and as_json:
            return json.dumps(data)
        return data

    def _need_forced_redirection(self, data):
        return any(
            [
                self.request.params.get('force_apply_redirection'),
                self.request.params.get('redirect'),
                self.form.get('invader_success_url'),
                self.form.get('invader_error_url'),
                'check_payment' in self.request.httprequest.path,
            ]
        )
        # TODO: I'm not sure this is needed for us... they are intercepting every call
        # or self._is_html_form_edition()

    def _handle_redirection(self, response, data):
        redirect_url = ''
        status = 302
        referer = self.request.httprequest.headers.environ.get('HTTP_REFERER')
        if response.status_code == 200:
            if data.get('redirect_to'):
                redirect_url = data['redirect_to']
            elif self.form.get('invader_success_url'):
                redirect_url = self.form['invader_success_url']
            elif referer:
                redirect_url = referer
        else:
            if self.form.get('invader_error_url'):
                redirect_url = self.form['invader_error_url']
            elif referer:
                redirect_url = referer
            else:
                response.raise_for_status()
        if redirect_url:
            return werkzeug.utils.redirect(redirect_url, status)

    def _prepare_result(self, response, data):
        if 'set_session' in data:
            self.request.session.update(data['set_session'])
        if 'store_cache' in data:
            data['store'] = data['store_cache']

    # def _is_html_form_edition(self, current_request):
    #     # if you do a post/put/delete from the browse directly with a basic html form
    #     # we process it as an html edition and we will do the redirection
    #     # parsing the http_accept is done in a simple way here
    #     method = current_request.httprequest.method
    #     accept = parse_http_accept_header(current_request.httprequest.headers.get('HTTP_ACCEPT'))
    #     if accept.size > 0 and method:
    #         return accept[0][0] == "text/html" and method in ('POST', 'PUT', 'DELETE')
    #     return False

    # def parse_http_accept_header(header)
    #     header.to_s.split(/\s*,\s*/).map do |part|
    #     attribute, parameters = part.split(/\s*;\s*/, 2)
    #     quality = 1.0
    #     if parameters and /\Aq=([\d.]+)/ =~ parameters
    #         quality = $1.to_f
    #     end
    #     [attribute, quality]
    #     end
