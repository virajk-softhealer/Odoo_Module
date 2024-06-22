# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, _


class ShLoyaltyPoint(models.TransientModel):
    _name = 'sh.loyalty.point'
    _description = 'Loyalty Point'
    
    sh_details = fields.Html(string='Details Loyalty Point')