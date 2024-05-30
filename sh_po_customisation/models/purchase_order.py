# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

from odoo import api, fields, models, tools

class PurchaseOrder(models.Model):
    _inherit= 'purchase.order'

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sh_sale_price = fields.Float(string='Sale Price')
    sh_available_quantity = fields.Float(string='Available Quantity',
    related='product_id.qty_available' )
    sh_barcode = fields.Char(string='Barcode',
    related='product_id.barcode')

    # ONCHANGE METHOD 
    @api.onchange('product_id')
    def onchange_product_sale_price(self):
        self.sh_sale_price = self.product_id.lst_price
