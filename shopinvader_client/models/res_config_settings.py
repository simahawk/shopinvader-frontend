from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    shopinvader_api_key_id = fields.Many2one(
        related='website_id.shopinvader_api_key_id', readonly=False
    )
    shopinvader_master_api_key = fields.Char(
        related='website_id.shopinvader_master_api_key', readonly=False
    )
    shopinvader_master_url = fields.Char(
        related='website_id.shopinvader_master_url', readonly=False
    )
