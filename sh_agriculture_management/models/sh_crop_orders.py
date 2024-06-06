# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api,_


class sh_crop_orders(models.Model):
    _name = "sh.crop.orders"
    _description = "Crop Orders"
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    name = fields.Char()
    partner_id = fields.Many2one("res.partner", string="Partner", required=True, tracking=True)
    sh_agriculture_crops_id = fields.Many2one(
        "sh.agriculture.crops", string="Agriculture Crop", required=True, tracking=True)
    sh_estimated_quantity = fields.Float(string="Estimated Quantity", required=True, readonly=True, tracking=True)
    sh_actual_qty = fields.Float(string='Actual Quantity',tracking=True)
    uom_id = fields.Many2one('uom.uom', readonly=True)

    process_start = fields.Date(string="Process Start", tracking=True)
    expected_delivery = fields.Date(string="Expected Delivery", tracking=True)
    actual_delivery = fields.Date(string="Actual Delivery", tracking=True)
    user_id = fields.Many2one("res.users", string="Inspector",
                              default=lambda self: self.env.user, tracking=True)
    farmer_id = fields.Many2one("res.partner", string="Crop Farmer",
                                 domain=[('farmer', '=', True)], tracking=True)
    company_id = fields.Many2one('res.company', string="Related Company",
                                    default=lambda self: self.env.company, tracking=True)
    order_note = fields.Text(" ")
    order_description = fields.Text(" ")
    sh_state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
        ], string='State', default='new')

    task_count = fields.Integer(compute='_compute_task_count')
    equipments_count = fields.Integer(compute='_compute_equipments_count')
    animal_count = fields.Integer(compute='_compute_animal_count')
    dieases_count = fields.Integer(compute='_compute_dieases_count')
    fleet_count = fields.Integer(compute='_compute_fleet_count')
    project_count = fields.Integer(compute='_compute_project_count')
    labours_count = fields.Integer(compute='_compute_labours_count')
    total_days_count = fields.Integer(compute='_compute_total_days_count')

    project_id = fields.Many2one(
        "project.project", "Related Project", readonly=True)
    task_name = fields.Char(' ')
    project_task_ids = fields.One2many("project.task", 'sh_crop_order_id')

    sale_order_id = fields.Many2one('sale.order', string="Related Sale Order")

    # Loss Reason page 
    sh_disease_crops_id = fields.Many2one('sh.disease.crops', readonly=True)
    disease_loss_crop = fields.Integer('', readonly=True)
    sh_incident_crops_id = fields.Many2one('sh.incident.crops',readonly=True)
    incident_loss_crop = fields.Integer('', readonly=True)
    sh_description = fields.Text(string="Description", readonly=True)
    loss_uom_id = fields.Many2one('uom.uom', readonly=True)


#  for show item count in smart button
    def _compute_task_count(self):
        for task in self:
            taskcount = self.env['project.task'].search(
                [('sh_crop_order_id', '=',  self.id)])
            task.task_count = len(taskcount)
            
    def _compute_equipments_count(self):
        for equipments in self:
            equipmentscount = self.env['sh.process.equipment'].search(
                [('sh_list_process_id.sh_agri_crops_id', '=', self.sh_agriculture_crops_id.id)])
            equipments.equipments_count = len(equipmentscount)
            
    def _compute_animal_count(self):
        for animal in self:
            animalcount = self.env['sh.process.animals'].search(
                [('sh_list_process_id.sh_agri_crops_id', '=', self.sh_agriculture_crops_id.id)])
            animal.animal_count = len(animalcount)

    def _compute_dieases_count(self):
        for dieases in self:
            dieasescount = self.env['sh.disease.crops'].search(
                [('sh_agri_crops_id', '=', self.sh_agriculture_crops_id.id)])
            dieases.dieases_count = len(dieasescount)
          

    def _compute_fleet_count(self):
        for fleet in self:
            fleetcount = self.env['sh.process.vehicles'].search(
                [('sh_list_process_id.sh_agri_crops_id', '=', self.sh_agriculture_crops_id.id)])
            fleet.fleet_count = len(fleetcount)
          
    def _compute_project_count(self):
        for project in self:
            projectcount = self.env['project.project'].search(
                [('sh_crop_order_id', '=', self.id)])
            project.project_count = len(projectcount)

    def _compute_labours_count(self):
        for rec in self:
            rec.labours_count = 0
            for temp in rec.project_task_ids:
                for lab in temp.sh_labour_ids:
                    rec.labours_count  += lab.total_labour
    
    def _compute_total_days_count(self):
        for rec in self:
            rec.total_days_count = 0
            for temp in rec.project_task_ids:
                for lab in temp.sh_labour_ids:
                    rec.total_days_count  += lab.total_days

# for button on header cleck to change state
    def action_confirm(self):
        self.sh_state = 'confirmed'

    # def action_cancel(self):
    #     self.sh_state = 'new'

    def action_in_progress(self):
        self.sh_state = 'in_progress'
        
     
        project = self.env['project.project'].create({
            'name': self.partner_id.name +'-'+ self.name,
            'sh_crop_order_id' : self.id,
            'is_agri_project' : True
            })
        self.project_id = project.id
        

        for process_list in self.sh_agriculture_crops_id.sh_list_process_ids:
            # print('\n\n\n......TASK......', process_list.sh_task_id.name)
            if process_list:


                task_equipment_lines=[]
                if process_list.sh_process_equipment_ids:
                    for equipment in process_list.sh_process_equipment_ids:
                        task_equipment_lines.append((0, 0, {
                            'equipment': equipment.equipment.id,
                            'serial_no': equipment.serial_no,
                            'alloted_date': equipment.alloted_date,
                            'owner': equipment.owner.id,
                            'technician': equipment.technician.id,
                            'equipment_category': equipment.equipment_category,
                        }))
                    
                task_animal_lines = []
                if process_list.sh_process_animals_ids:
                    for animal in process_list.sh_process_animals_ids:
                        task_animal_lines.append((0, 0, {
                            'animal_id': animal.animal_id.id,
                            'total_animal': animal.total_animal,
                            'begin_date': animal.begin_date,
                            'finish_date': animal.finish_date,
                            'animal_description': animal.animal_description,
                        }))
                task_vehicle_lines = [] 
                if process_list.sh_process_vehicles_ids:
                    for vehicle in process_list.sh_process_vehicles_ids:
                        task_vehicle_lines.append((0, 0, {
                            'sh_agri_vehicles_id': vehicle.sh_agri_vehicles_id.id,
                            # 'total_vehicle': vehicle.total_vehicle,
                            'begin_date': vehicle.begin_date,
                            'finish_date': vehicle.finish_date,
                            'description': vehicle.description,
                            }))
                        
                task_labour_lines = [] 
                if process_list.sh_labour_ids:
                    for labour in process_list.sh_labour_ids:
                        task_labour_lines.append((0, 0, {
                            'name': labour.name,
                            'total_labour': labour.total_labour,
                            'begin_date': labour.begin_date,
                            'finish_date': labour.finish_date,
                            'total_days': labour.total_days,
                            'description': labour.description,
                            }))

                self.env['project.task'].create({
                        'name': process_list.sh_task_id.name+'-'+self.name,
                        'partner_id':self.partner_id.id,
                        'project_id':self.project_id.id,
                        'sh_crop_order_id':self.id,
                        'sh_agriculture_crops_id': self.sh_agriculture_crops_id.id,
                        'is_agri_task': False,
                        'sh_process_equipment_ids': task_equipment_lines,
                        'sh_process_animals_ids': task_animal_lines,
                        'sh_process_vehicles_ids': task_vehicle_lines,
                        'sh_labour_ids': task_labour_lines,
                    })
        
       
    def action_done(self):
        
        if self.sh_actual_qty < self.sh_estimated_quantity:
            self.sh_state = 'in_progress'
            # print("\n\n\n\nCrop ORDER",self.sh_agriculture_crops_id)
            return {
                'type': 'ir.actions.act_window',
                'name': _('Reason For Less Than Estimated Quantity'),
                'view_mode': 'form',
                'res_model': 'sh.less.qty.reason.wizard',
                'views': [(False, 'form')],
                'view_id': False,
                'target': 'new',
                'context':{
                    'default_loss_uom_id':self.uom_id.id
                }
            }
        else:
            self.sh_state = 'done'
            stock_count = self.env['stock.quant'].search(
                [('product_id', '=', self.sh_agriculture_crops_id.product_id.id),
                ('location_id', '=', self.sh_agriculture_crops_id.sh_crops_stock_location_id.id)])
            if stock_count:
                self.sh_agriculture_crops_id.update({
                        'qty_available': stock_count.quantity + self.sh_actual_qty
                    })
                stock_count.update({
                        'quantity': self.sh_agriculture_crops_id.qty_available
                    })                   
            else:
                self.sh_agriculture_crops_id.update({
                    'qty_available': stock_count.quantity + self.sh_actual_qty
                })
                stock_count.create({
                    'quantity': self.sh_agriculture_crops_id.qty_available,
                    'product_id':self.sh_agriculture_crops_id.product_id.id,
                    'location_id': self.sh_agriculture_crops_id.sh_crops_stock_location_id.id,
                })

    

#  for auto increment order Number
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            next_number = self.env['ir.sequence'].sudo(
            ).next_by_code('crop.orders')
          
            vals['name'] = next_number

        return super(sh_crop_orders, self).create(vals_list)
    


    def action_view_task(self):
        self.ensure_one()
        # task = self.env.ref(
        #     'project.action_view_task').read()[0]
        task = self.env["ir.actions.actions"]._for_xml_id("project.action_view_task")

        task['domain'] = [
            ('sh_crop_order_id', '=',  self.id)]
        # print("\n\n\n\n\n==========", task['domain'])
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'project.task',
            'domain': task['domain'],
            'views': [(False, 'tree'), (False, 'form')],
            'view_id': False,
            "name": ("Crop Task"),
            'target': 'action_view_task',

        }

    def action_view_equipments(self):
        equipment = self.env["ir.actions.actions"]._for_xml_id("sh_agriculture_management.sh_crops_processes_equipment_action")
        equipment['domain'] = [
            ('sh_list_process_id.sh_agri_crops_id', '=', self.sh_agriculture_crops_id.id)]
        
        result = {
            "type": "ir.actions.act_window",
            "res_model": "sh.process.equipment",
            "domain": equipment['domain'],
            "name": _("Crop Equipments"),
            'view_mode': 'tree,form',
        }
        return result
        # self.ensure_one()
        # equipment = self.env.ref(
        #     'sh_agriculture_management.sh_crops_processes_equipment_action').read()[0]
    
        # equipment['domain'] = [
        #     ('sh_list_process_id.sh_agri_crops_id', '=', self.sh_agriculture_crops_id.id)]

        # return {
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'tree',
        #     'res_model': 'sh.process.equipment',
        #     'domain': equipment['domain'],
        #     'views': [(equipment.id, 'tree')],
        #     'view_id': equipment.id,
        #     "name": ("Crop Equipments"),
        #     'target': 'new',
           
        # }
    

    def action_view_animal(self):
        self.ensure_one()
        # animal = self.env.ref(
        #     'sh_agriculture_management.sh_crops_processes_animal_action').read()[0]
        animal = self.env["ir.actions.actions"]._for_xml_id("sh_agriculture_management.sh_crops_processes_animal_action")
       
        animal['domain'] = [
            ('sh_list_process_id.sh_agri_crops_id', '=', self.sh_agriculture_crops_id.id)]

        return {
           'type': 'ir.actions.act_window',
           'view_mode': 'tree',
           'res_model': 'sh.process.animals',
           'domain': animal['domain'],
           'views': [(False, 'tree')],
           'view_id': False,
           "name": ("Crop Animals"),
           'target': 'sh_crops_processes_animal_action',
       }

    def action_view_dieases(self): 
        self.ensure_one()
        # dieases = self.env.ref(
        #     'sh_agriculture_management.sh_diseaes_crops_action').read()[0]
        dieases = self.env["ir.actions.actions"]._for_xml_id("sh_agriculture_management.sh_diseaes_crops_action")
        
        dieases['domain'] = [
            ('sh_agri_crops_id', '=', self.sh_agriculture_crops_id.id)]

        return {
           'type': 'ir.actions.act_window',
           'view_mode': 'tree',
           'res_model': 'sh.disease.crops',
           'domain': dieases['domain'],
           'views': [(False, 'tree')],
           'view_id': False,
           "name": ("Crop Disease"),
           'target': 'current',
       }
    
    def action_view_fleet(self):
        self.ensure_one()
        # fleet = self.env.ref(
        #     'sh_agriculture_management.sh_crops_processes_vehicles_action').read()[0]
        fleet = self.env["ir.actions.actions"]._for_xml_id("sh_agriculture_management.sh_crops_processes_vehicles_action")

        fleet['domain'] = [
            ('sh_list_process_id.sh_agri_crops_id', '=', self.sh_agriculture_crops_id.id)]

        # print("\n\n\n\nFeet",fleet['domain'])
        return {
            'type': 'ir.actions.act_window',
            'view_mode':'tree',
            'res_model':'sh.process.vehicles',
            'domain': fleet['domain'],
            'views': [(False, 'tree')],
            'view_id': False,
            "name": ("Crop Fleet"),
            'target': 'sh_crops_processes_vehicles_action',
        }
    
    def action_view_project(self):
        self.ensure_one()
        # project = self.env.ref(
        #     'project.open_view_project_all').read()[0]
        project = self.env["ir.actions.actions"]._for_xml_id("project.open_view_project_all")
        project['domain'] = [
            ('sh_crop_order_id', '=', self.id)]
        
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'project.project',
            'domain': project['domain'],
            'views': [(False, 'tree'), (False, 'form')],
            'view_id': False,
            "name": ("Agriculture Project"),
            'target': 'open_view_project_all',
        }

    def action_view_labours(self):
        pass
        # print('\n\n\n\n===Self',self)