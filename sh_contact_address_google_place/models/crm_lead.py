# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
import json


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sh_contact_google_location = fields.Char('Enter Location')

    sh_contact_place_text = fields.Char('Enter location', copy=False)
    sh_contact_place_text_main_string = fields.Char(
        'Enter location ', copy=False)

    # ONCHANGE METHOD 

    @api.onchange('sh_contact_place_text_main_string')
    def onchange_crm_lead_technical_main_string(self):
        if self.sh_contact_place_text_main_string:
            print("\n\n\n sh_contact_place_text_main_string",self.sh_contact_place_text_main_string)
            self.sh_contact_google_location = self.sh_contact_place_text_main_string
            print("\n\n\n sh_contact_google_location",self.sh_contact_google_location)


    @api.onchange('sh_contact_place_text')
    def onchange_crm_lead_goofle_text(self):

        if self.sh_contact_place_text:
            crm_lead_google_place_text = json.loads(self.sh_contact_place_text)

            if crm_lead_google_place_text:
                self.street = crm_lead_google_place_text.get('street')
        
  