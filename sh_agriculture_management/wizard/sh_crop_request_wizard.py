# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime


class sh_crop_request_wizard(models.Model):
    _name = "sh.crop.request.wizard"
    _description = "Crop Request Wizard"

    crop_id = fields.One2many(
        "sh.crop.request", 'request_crop_id', string="Crop")

    def crop_request_create(self):
        orders = self.env["sh.crop.orders"]
        for res in self.crop_id:
            crop_order_val = orders.create({
                "partner_id" : res.partner_id.id,
                "user_id" : res.user_id.id,
                "process_start" : res.being_date,
                "expected_delivery": res.finish_date,
                "sh_agriculture_crops_id": res.sh_agriculture_crops_id.id,
                "sh_estimated_quantity": res.estimated_quantity,
                "farmer_id": res.farmer_id.id,
                'uom_id': res.crop_uom_id.id,
                'sale_order_id':res.sale_order_id.id
            })
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'sh.crop.orders',
            'views': [(False, 'tree')],
            'domain': [('partner_id', '=', res.partner_id.id), ('farmer_id', '=', res.farmer_id.id)],
            'view_id': False,
            "name": ("Crop Orders"),
            'target': 'sh.crop.orders',
            'context': crop_order_val.id,
        }
