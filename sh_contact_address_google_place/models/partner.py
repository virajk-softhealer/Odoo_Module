# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
import json


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sh_contact_google_location = fields.Char('Enter Location')

    sh_contact_place_text = fields.Char('Enter location', copy=False)
    sh_contact_place_text_main_string = fields.Char(
        'Enter location ', copy=False)

    @api.onchange('sh_contact_place_text_main_string')
    def onchange_technical_google_text_main_string(self):
        """to save name in google field"""
        if self.sh_contact_place_text_main_string:
            self.sh_contact_google_location = self.sh_contact_place_text_main_string

    @api.onchange('sh_contact_place_text')
    def onchange_technical_google_text(self):
        """to place info to std. address fields"""
        if self.sh_contact_place_text:
            google_place_dict = json.loads(self.sh_contact_place_text)
            if google_place_dict:
                self.zip = google_place_dict.get('zip', '')
                self.street = google_place_dict.get('formatted_street','') or f'{google_place_dict.get("number","")} {google_place_dict.get("street","")}'
                self.country_code=google_place_dict.get('country_code','')
                self.city=google_place_dict.get('city','')
                self.country_id=google_place_dict.get('country',False)
                self.state_id=google_place_dict.get('state',False)
