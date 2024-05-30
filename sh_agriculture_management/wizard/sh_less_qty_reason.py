# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime


class ShLessQtyReason(models.Model):
    _name = "sh.less.qty.reason.wizard"
    _description = "Less Quantity Reason Wizard"

    sh_disease_incident= fields.Selection(
        [('disease_crops','Show Disease'),
         ('incident_crops', 'Show Incident'),
         ('both', 'Both')],
        string="Which Type of Loss",
        default="disease_crops")
    sh_disease_crops_id = fields.Many2one('sh.disease.crops')
    disease_loss_crop = fields.Integer('')
    sh_incident_crops_id = fields.Many2one('sh.incident.crops')
    incident_loss_crop = fields.Integer('')
    sh_description = fields.Text(string="Description")
    loss_uom_id = fields.Many2one('uom.uom', readonly=True)

    def less_qty_reason(self):
        active_id = self.env.context.get('active_id')
        crop_order = self.env['sh.crop.orders'].browse(active_id)
        crop_order.write({
            'sh_disease_crops_id': self.sh_disease_crops_id.id,
            'disease_loss_crop': self.disease_loss_crop,
            'sh_incident_crops_id': self.sh_incident_crops_id.id,
            'incident_loss_crop': self.incident_loss_crop,
            'sh_description': self.sh_description,
            'loss_uom_id':self.loss_uom_id.id,
            'sh_state':'done'
            })
        if crop_order.sh_agriculture_crops_id:
            stock_count = self.env['stock.quant'].search(
                [('product_id', '=', crop_order.sh_agriculture_crops_id.product_id.id),
                ('location_id', '=', crop_order.sh_agriculture_crops_id.sh_crops_stock_location_id.id)])
            if stock_count:
                crop_order.sh_agriculture_crops_id.update({
                        'qty_available': stock_count.quantity + crop_order.sh_actual_qty
                    })
                stock_count.update({
                        'quantity': crop_order.sh_agriculture_crops_id.qty_available
                    })                   
            else:
                crop_order.sh_agriculture_crops_id.update({
                    'qty_available': stock_count.quantity + crop_order.sh_actual_qty
                })
                stock_count.create({
                    'quantity': crop_order.sh_agriculture_crops_id.qty_available,
                    'product_id':crop_order.sh_agriculture_crops_id.product_id.id,
                    'location_id': crop_order.sh_agriculture_crops_id.sh_crops_stock_location_id.id,
                })

