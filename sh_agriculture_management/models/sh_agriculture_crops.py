# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api,_
from odoo.exceptions import UserError

class sh_agriculture_crops(models.Model):
    _name = "sh.agriculture.crops"
    _description = "this model for agriculture crops"
    _rec_name = 'product_id'

    # name = fields.Char(string="Name", required=True)
    sh_crops_img = fields.Binary()
    sh_crops_duration = fields.Integer(string="Crops Duration", required=True)
    sh_crop_duration_day = fields.Char(default="days", readonly=True)
    sh_crop_season = fields.Many2one(
        'sh.season', string="Crop Season", required=True)
    sh_crops_warehouse_id = fields.Many2one(
        "stock.warehouse", string="Crop Warehouse", required=True)
    sh_crops_stock_location_id = fields.Many2one(
        "stock.location", string="Crops Stock Location", required=True)
    sh_crops_description = fields.Text(string="Crops Description")
    qty_available = fields.Float(
        'Quantity On Hand', compute='_compute_qty_available')

    product_id = fields.Many2one('product.product', string="Product", required=True)
    sh_crop_raw_material_ids = fields.One2many(
        'sh.crop.raw.material', 'sh_agri_crops_id', string="Crop raw material")
    
    # sh_crop_labours_ids = fields.One2many(
    #     'sh.crop.labours', 'sh_agri_crops_id', string="Crop Labours")
    
    # sh_crop_overhead_ids = fields.One2many(
    #     'sh.crop.overhead', 'sh_agri_crops_id', string="Crop Overhead")
    
    sh_diseaescrops_ids = fields.One2many(
        'sh.disease.crops', 'sh_agri_crops_id', string="Crop Disease")
    # sh_diseaes_crops_ids = fields.Many2many(
    #     'sh.disease.crops', string="Crop Disease")
    
    sh_list_process_ids = fields.One2many(
        'sh.list.process', 'sh_agri_crops_id', string="List Process")
    
    sh_soil_ids = fields.One2many(
        'sh.soil', 'sh_agri_crops_id', string="Preferred Soil")
    
    sh_soil_id = fields.Many2one(
        'sh.soil', string="Preferred Soil")
    
    sh_crop_condition_ids = fields.One2many(
        'sh.crop.condition', 'sh_agri_crops_id', string="Crop Conditions")

    sh_duration_total_days = fields.Integer(
        compute="_compute_sh_duration_total_days")

    sh_crop_info_message = fields.Char(default='Raw material and processes qty and duration are based on the per unit production of the crop')
    
    
    def action_crops_quants(self):
        if len(self) == 1:
            self = self.with_context(
                default_product_id=self.product_id.id,
                default_location_id=self.sh_crops_stock_location_id.id,
                single_product=True
            )
        else:
            self = self.with_context(product_id=self.product_id.ids)
        action = self.env['stock.quant'].action_view_inventory()
        # note that this action is used by different views w/varying customizations
        if not self.env.context.get('is_stock_report'):
            action['domain'] = [('product_id', 'in', self.product_id.ids),
                                ('location_id', '=', self.sh_crops_stock_location_id.id)]
            action["name"] = _('Update Quantity')
        return action
        
    def _compute_qty_available(self):
        for available_quantity in self:
            stock_count = self.env['stock.quant'].search(
                [('product_id', '=', self.product_id.id),
                 ('location_id', '=', self.sh_crops_stock_location_id.id)])
            available_quantity.qty_available = stock_count.quantity

    @api.depends('sh_list_process_ids')
    def _compute_sh_duration_total_days(self):
        for rec in self:
            rec.sh_duration_total_days = 0
            total_days = 0
            for day in rec.sh_list_process_ids:
                total_days += day.sh_duration
            rec.sh_duration_total_days = total_days
        if rec.sh_duration_total_days > rec.sh_crops_duration:
            raise UserError(_('Enter Valid Process Duration'))
        
    
