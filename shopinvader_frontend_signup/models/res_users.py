# -*- coding: utf-8 -*-
# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from odoo.http import request
from werkzeug.datastructures import ImmutableOrderedMultiDict
from ...shopinvader_client.components.mixin import ProxyConsumerMixin
import logging

_logger = logging.getLogger(__name__)


class ResUsers(models.Model, ProxyConsumerMixin):
    _inherit = "res.users"

    is_shop_customer = fields.Boolean(string="Shop customer")

    def _signup_create_user(self, values):
        """Configure a new registred user as a shop user.

        Sets the proper security group and create the corresponding partner
        on Odoo Master.
        """
        values['is_shop_customer'] = True
        values['groups_id'] = [(
            4,
            self.env.ref('base.group_portal').id,
            False
        )]
        user = super()._signup_create_user(values)
        user._invader_create_customer()
        return user

    def _invader_create_customer(self):
        """Create a partner on Odoo Master.

        Some required params are set with default value, for now.
        """
        payload = self._invader_new_customer_values()
        # TODO: handle possible errors
        with self.work_on_proxy(form=payload) as work:
            proxy = work.component(usage='proxy')
            rest_resp = proxy.make_request('/customer/create', method='POST')
            _logger.info('Shopinvader customer created: %s', self.partner_id.email)
            _logger.info('REST API info: %s', str(rest_resp))
        return rest_resp

    def _invader_new_customer_values(self):
        return ImmutableOrderedMultiDict([
            ('email', self.partner_id.email),
            ('name', self.partner_id.name),
            # TODO
            ('country', {'id': self.env.ref("base.ch").id}),
            ('zip', 'zip'),
            ('street', 'street'),
            ('city', 'city'),
            ('external_id', 'external_id'),
            # ('lang', ),
        ])

    @classmethod
    def authenticate(cls, db, login, password, user_agent_env):
        uid = super().authenticate(db, login, password, user_agent_env)
        cls._invader_authenticate_customer(db, uid)
        return uid

    @classmethod
    def _invader_authenticate_customer(cls, cr, uid):
        with cls.pool.cursor() as cr:
            env = api.Environment(cr, uid, {})
            user = env['res.users'].browse(uid)
            user_email = user.login if user.is_shop_customer else ''
            if user_email:
                _logger.info('Shopinvader customer login: %s', user_email)
                # TODO: handle possible errors
                with user.work_on_proxy(user=user) as work:
                    proxy = work.component(usage='proxy')
                    proxy.make_request('/customer/sign_in', method='POST')
