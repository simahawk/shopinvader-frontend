# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from contextlib import contextmanager

from odoo.addons.base_rest.controllers.main import _PseudoCollection
from odoo.addons.component.core import WorkContext
from odoo.http import request


class ProxyConsumerMixin(object):
    """Inheritable mixin class to add proxy-consumer feature."""

    _proxy_collection_name = 'shopinvader.proxy'

    @property
    def proxy_collection(self):
        return _PseudoCollection(self._proxy_collection_name, request.env)

    @contextmanager
    def work_on_proxy(self, form=None, user=None, **kw):
        params = self._get_proxier_context(form=form, user=user)
        params.update(kw)
        yield WorkContext(
            model_name='website',
            collection=self.proxy_collection,
            **params
        )

    def _get_proxier_context(self, form=None, user=None):
        return {
            'request': request,
            'form': form or request.httprequest.form,
            'user': user or request.env.user,
        }