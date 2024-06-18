# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class ShStoreWiseSMSAllocation(models.Model):
    _name = 'sh.store.wise.sms.allocation'
    _description = "Store Wise SMS Allocation"

    
    sh_twilio_account_id = fields.Many2one(
        string='Account Reference',
        comodel_name='sh.twilio.account',
        ondelete='cascade',
    )
    sh_store = fields.Char(string='Store')
    sh_allocates_sms = fields.Char(string='Allocated SMS')
    