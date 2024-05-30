# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

from odoo import api, fields, models, tools, _


class ShPosBoolUpdate(models.TransientModel):
    _name = 'sh.pos.bool.update'
    _description = 'Sh Pos Bool Update'

    sh_pos_bool = fields.Boolean(string='Available in POS',default=True)
    
    # POS_BOOLEAN UPDATE METHOD CREATE 
    def update_pos_bool(self):
        context = self.env.context.copy()
        
        if context.get('active_ids'):
            
            product_id = context.get('active_ids')
            
            if self.sh_pos_bool:
                product_template_id = self.env['product.template'].sudo().browse([r for r in product_id]).write({"available_in_pos":True})

            else:
                product_template_id = self.env['product.template'].sudo().browse([r for r in product_id]).write({"available_in_pos":False})


class ProductTemplate(models.Model):
    _inherit= 'product.template'

    # MASS ACTION CREATE 
    def action_mass_available_pos_bool_update(self):

        # WIZARD  OPEN 
        return{
            'name': _('Update'),
            'type':'ir.actions.act_window',
            'res_model':'sh.pos.bool.update',
            'view_mode':'form',
            'target':'new'
        }

