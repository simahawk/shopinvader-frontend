from odoo import api, fields, models, tools

# from odoo.addons.http_routing.models.ir_http import slugify
import logging

_logger = logging.getLogger(__name__)
try:
    import addict
except ImportError:
    _logger.error('`addict` lib is required')


class Website(models.Model):
    _name = "website"
    _inherit = [
        "website",
        # we have components registered for website
        "collection.base",
    ]

    shopinvader_api_key_id = fields.Many2one(
        "auth.api.key",
        help="Key that identifies this specific website "
             "for calls from Odoo master. "
             "Odoo master will use this key to export - for instance - "
             "its global settings to the Odoo client. "
             "It must be configured on Shopinvader backend on Odoo master."
    )
    # TODO: use api key id
    shopinvader_master_api_key = fields.Char(
        required=True,
        help="Key used to call Odoo master for data retrieval via REST API. "
             "It must be configured on Odoo master via env file "
             "and selected on Shopinvader backend on Odoo master."
    )
    shopinvader_master_url = fields.Char(
        required=True,
        help='Complete URL of Odoo master instance. '
             'Eg: http://odoo.master:8069'
    )
    shopinvader_master_settings = fields.Serialized(
        help="Holds configuration data from odoo master."
    )
    # No nice widget, let's make settings visible in backend UI
    shopinvader_master_settings_display = fields.Text(
        compute='_compute_shopinvader_master_settings_display'
    )

    @api.depends('shopinvader_master_settings')
    def _compute_shopinvader_master_settings_display(self):
        for rec in self:
            if not rec.shopinvader_master_settings:
                continue
            # TODO: improve
            rec.shopinvader_master_settings_display = '\n'.join(
                [
                    '{}: {}'.format(k, str(v))
                    for k, v in rec.shopinvader_master_settings.items()
                ]
            )

    @api.model
    @tools.ormcache("self._uid", "auth_api_key_id")
    def _get_id_from_auth_api_key(self, auth_api_key_id):
        return self.search([("shopinvader_api_key_id", "=", auth_api_key_id)]).id

    @api.model
    def _get_from_http_request(self, current_request):
        auth_api_key_id = getattr(current_request, "auth_api_key_id", None)
        return self.browse(self._get_id_from_auth_api_key(auth_api_key_id))

    @api.multi
    def get_invader_settings(self):
        """Retrieve invader global settings.

        Mostly coming from Odoo master exports.
        """
        self.ensure_one()
        return self.shopinvader_master_settings

    @api.multi
    def update_invader_settings(self, values):
        """Update global invader settings.

        Existing keys are replaced.
        """
        self.ensure_one()
        settings = self.shopinvader_master_settings or {}
        settings.update(values)
        self.write({'shopinvader_master_settings': settings})
        return settings

    def invader_countries(self, lang='en_US'):
        lang = lang.split('_')[0]
        settings = self.get_invader_settings()
        return settings['available_countries'].get(lang, [])

    # TODO: move to another helper model
    ORDER_STATE_COLOR_MAP = addict.Dict({
        'default': {
            'color': 'primary',
            'level': 0,
        },
        'pending': {
            'color': 'info',
            'level': 1,
        },
        'processing': {
            'color': 'warning',
            'level': 2,
        },
        'done': {
            'color': 'success',
            'level': 3,
        },
    })

    def order_state_info(self, state):
        return self.ORDER_STATE_COLOR_MAP.get(state, self.ORDER_STATE_COLOR_MAP['default'])