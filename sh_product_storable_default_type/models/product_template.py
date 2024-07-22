# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def default_get(self, fields_list):
        default_vals = super(ProductTemplate, self).default_get(fields_list)

        default_vals['detailed_type'] = 'product'

        return default_vals

    def sh_action_detailed_type(self):
        query = """ 
            UPDATE product_template SET detailed_type = 'product', type = 'product'
                WHERE detailed_type = 'consu'
                RETURNING id;         
        """

        self.env.cr.execute(query)

        product_ids = [row[0] for row in self._cr.fetchall()]
        print('\n\n\n product_ids',product_ids)
        _logger.info("%s products's updated successfully: %s", len(product_ids),product_ids)
