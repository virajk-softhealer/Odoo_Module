# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies

from odoo import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def default_get(self, fields_list):
        default_vals = super(ProductProduct, self).default_get(fields_list)

        default_vals['available_in_pos'] = True

        return default_vals
