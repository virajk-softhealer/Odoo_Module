# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
from datetime import datetime


class ShERPMasterDashboard(models.Model):
    _name = 'sh.erp.master.dashboard'
    _description = 'ERP Master Dashboard'

    # name = fields.Char("")

    def get_erp_master_dashboard_details(self):
        return self.env['sh.client.shop']._get_shop_data()
