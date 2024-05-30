# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api,_
from odoo.exceptions import  ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    hide_crop_btn = fields.Boolean(compute='_compute_hide_crop_btn')

    def _compute_hide_crop_btn(self):
        for rec in self:
            rec.hide_crop_btn = False
            for line in rec.order_line:
                if line.product_id.is_agri == True and line.product_id.agri_crop == True or line.product_template_id.is_agri == True and line.product_template_id.agri_crop == True:
                    rec.hide_crop_btn = True
                    

    def sh_crop_request_wizard_action(self):
        if self.order_line:
            sale_order_lines = []
            
            for line in self.order_line:

                agri_crop = self.env['sh.agriculture.crops'].search(
                    [('product_id', '=', line.product_id.id),])
                if not agri_crop:
                    agri_crop = self.env['sh.crop.raw.material'].search(
                        [('product_id', '=', line.product_id.id),])
                    if not agri_crop:
                        agri_crop = self.env['sh.crop.labours'].search(
                            [('product_id', '=', line.product_id.id),])
                        if not agri_crop:
                            agri_crop = self.env['sh.crop.overhead'].search(
                                [('product_id', '=', line.product_id.id),])
                    
                
                if line.product_id.is_agri and line.product_id.agri_crop:
                    
                    for res in agri_crop:
                        sale_order_lines.append((0, 0, {
                            'partner_id': self.partner_id.id,
                            'sh_agriculture_crops_id': res.id,
                            'estimated_quantity': line.product_uom_qty,
                            'crop_uom_id': line.product_uom.id,
                            'sale_order_id':self.id

                        }))
                    
                


                ctx ={
                    'default_crop_id': sale_order_lines,
                    }
               
            
            return {
                'type': 'ir.actions.act_window',
                'name': _('Create Crop Request'),
                'view_mode': 'form',
                'res_model': 'sh.crop.request.wizard',
                'views': [(False, 'form')],
                'view_id': False,
                'target': 'new',
                'context': ctx,
            }
