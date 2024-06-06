# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

from odoo import api, fields, models, tools,Command
from datetime import date 
class PurchaseOrder(models.Model):
    _inherit= 'purchase.order'

    # METHOD INHERIT 
    def button_confirm(self):
        res = super(PurchaseOrder,self).button_confirm()

        # RECEIPT GENERATE 
        if self.picking_ids:
            for  picking in filter(lambda e:e .state =="assigned",self.picking_ids):

                    # PICKING VALIDATE 
                    picking.button_validate()

                    wizard_record = self.env['stock.immediate.transfer'].create({
                        'pick_ids':[(4,picking.id)],
                        'immediate_transfer_line_ids':[Command.create({
                            'picking_id':picking.id,
                            'to_immediate':True,
                        })]
                    })

                    # Transient MODEL METHOD CALL 
                    Process_btn = wizard_record.with_context(
                    button_validate_picking_ids=picking.ids).process()
        
        # CREATE BILL 
        self.action_create_invoice()
        
        if self.invoice_ids:
            bill = self.invoice_ids[0]

            # Today Date Added 
            bill.write({
                'invoice_date':date.today()})

            bill.action_post()

        return res

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sh_sale_price = fields.Float(string='Sale Price')
    sh_available_quantity = fields.Float(string='Available Quantity',
    related='product_id.qty_available' )
    sh_barcode = fields.Char(string='Barcode',
    related='product_id.barcode')

    price_unit = fields.Float(
        string='Unit Price', required=True, digits=(12,3),
        compute="_compute_price_unit_and_date_planned_and_name", readonly=False, store=True)

    # ONCHANGE METHOD 
    @api.onchange('product_id')
    def onchange_product_sale_price(self):
        self.sh_sale_price = self.product_id.lst_price


   