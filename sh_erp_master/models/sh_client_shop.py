# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import datetime
import uuid
from odoo import api, fields, models, Command


class ShClientShop(models.Model):
    _name = "sh.client.shop"
    _description = "Client Shop"
    # _rec_name = "name"
    # _order = "name"

    name = fields.Char(string="Name", copy=False)
    access_token = fields.Char(string="Access Token", readonly="1", copy=False)
    log_line = fields.One2many('sh.erp.log', 'shop_id', string='Log Line')

    def _log(self, message):
        self.env['sh.erp.log'].create({
            'name': message,
            'shop_id': self.id
        })

    def get_sub_id(self):
        sub_id = str(uuid.uuid4())
        if not self.search_count([('access_token', '=', sub_id)]):
            return sub_id
        return self.get_sub_id()

    @api.model_create_multi
    def create(self, vals_list):
        shops = super().create(vals_list)
        for shop in shops:
            shop.access_token = self.get_sub_id()
        return shops


    def _process_shop_data(self, data):
        create_count = 0
        update_count = 0
        for pos_order_dict in data:
        
            pos_order_id = self.env['sh.pos.order'].sudo().search([('sh_shop_id','=',self.id),('res_id','=',pos_order_dict.get('res_id'))])
            order_vals = {
                'sh_shop_id' : self.id,
                'res_id' : pos_order_dict.get('res_id'),
                'name' : pos_order_dict.get('name'),
                'sh_pos_session_id' : pos_order_dict.get('session_id'),
                'date_order' : pos_order_dict.get('date_order'),
                'amount_tax' : pos_order_dict.get('amount_tax'),
                'amount_total' : pos_order_dict.get('amount_total'),
                'amount_paid' : pos_order_dict.get('amount_paid'),
            }

            if 'session_data' in pos_order_dict:
                session_id=self._get_session(pos_order_dict['session_data'])
                order_vals.update({'sh_pos_session_id' : session_id})

            if 'partner_data' in pos_order_dict:
                partner_id = self._get_customer(pos_order_dict.get('partner_data'))
                order_vals.update({'partner_id' : partner_id})
            
            if not pos_order_id:
                pos_order_id = self.env['sh.pos.order'].sudo().create(order_vals)
                create_count += 1
            else:
                pos_order_id.write(order_vals)
                update_count += 1

            if pos_order_id:
                order_line = []
                if 'order_line' in pos_order_dict:
                    for line in pos_order_dict.get('order_line'):
                        vals = {
                                'name' : line.get('name') or '',
                                'res_id' : line.get('res_id') or False,
                                'full_product_name' : line.get('full_product_name'),
                                'qty' : line.get('qty'),
                                'price_unit' : line.get('price_unit'),
                                'discount' : line.get('discount'),
                                'price_subtotal' : line.get('price_subtotal'),
                                'price_subtotal_incl' : line.get('price_subtotal_incl'),
                            }
                        
                        pos_order_line_id = self.env['sh.pos.order.line'].sudo().search([('res_id','=',line.get('res_id')),('sh_pos_order_id','=',pos_order_id.id)])
                        if not pos_order_line_id:
                            order_line.append((0,0, vals))
                        else:
                            pos_order_id.write({
                                'sh_pos_order_line': [
                                    Command.update(pos_order_line_id.id, vals),
                                ],
                            })
                
                    pos_order_id.write({'sh_pos_order_line': order_line})
                
                payment_line = []
                if 'payment_line' in pos_order_dict:
                    for line in pos_order_dict.get('payment_line'):
                        payment_vals = {
                                'name' : line.get('name') or '',
                                'res_id' : line.get('res_id') or False,
                                'partner_id' : pos_order_id.partner_id.id or False,
                                'payment_method' : line.get('payment_method'),
                                'amount' : line.get('amount'),
                                'payment_date' : datetime.strptime(line.get('payment_date'), '%m/%d/%Y %H:%M:%S'),
                            }

                        pos_payment_line_id = self.env['sh.pos.payment'].sudo().search([('res_id','=',line.get('res_id')),('sh_pos_order_id','=',pos_order_id.id)])
                        if not pos_payment_line_id:
                            payment_line.append((0,0, payment_vals))
                        else:
                            pos_order_id.write({
                                'sh_pos_payment_line': [
                                    Command.update(pos_payment_line_id.id, payment_vals),
                                ],
                            })
                    pos_order_id.write({'sh_pos_payment_line': payment_line})

        # Log in the shop
        msg_list = []
        if create_count:
            msg_list.append(f"{create_count} POS Orders created.")
        if update_count:
            msg_list.append(f"{update_count} POS Orders updated.")

        message = ''
        if msg_list:
            message = ', '.join(msg_list)
            self._log(message)

        return {
            'success': message
        }


    def get_records_current_year(self, model, datetime_field):
        # Get the current date
        today = fields.Date.today()

        # Calculate the start and end of the current year
        # start_of_year = today.replace(month=1, day=1)
        # end_of_year = today.replace(month=12, day=31, hour=23, minute=59, second=59)
        start_of_year = datetime(today.year, 1, 1, 0, 0, 0)
        end_of_year = datetime(today.year, 12, 31, 23, 59, 59)

        # Search domain to filter records within the current year
        domain = [
            (datetime_field, '>=', start_of_year),
            (datetime_field, '<=', end_of_year),
            # ('sh_shop_id', '=', self.id)
        ]

        # Search for records that match the domain
        records = self.env[model].search(domain)

        # # Example action: print the names of the records
        # for record in records:
        #     print(record.name)  # Replace with the desired action

        return records

    def _get_sales_data_list(self):
        pos_order = self.get_records_current_year('sh.pos.order', 'date_order')
        pos_order_lines = []
        payment_lines = []
        for order in pos_order:
            for order_line in order.sh_pos_order_line:
                pos_order_lines.append(order_line)
            # payment_lines.append(order.sh_pos_payment_line)
            for payment_line in order.sh_pos_payment_line:
                payment_lines.append(payment_line)
        # pos_order_lines = self.get_records_current_year('sh.pos.order', 'date_order')

        sales_dict = {
            'day': {
                'title': "Sales for Day",
                'total': 0.0,
                'payment_list': [],
                'total_tax': 00.00
            },
            'week': {
                'title': "Sales for Week",
                'total': 0.0,
                'payment_list': [],
                'total_tax': 00.00
            },
            'month': {
                'title': "Sales for Month",
                'total': 0.0,
                'payment_list': [],
                'total_tax': 00.00
            },
            'year': {
                'title': "Sales for Year",
                'total': 0.0,
                'payment_list': [],
                'total_tax': 00.00
            }
        }

        today_obj = datetime.today()
        current_day = today_obj.day
        current_week = today_obj.weekday
        current_month = today_obj.month
        # current_year = today_obj.year

        # total_price_subtotal_incl = 0.0
        # total_tax = 0.0
        if pos_order_lines:
            for line in pos_order_lines:
                # if current_day ==
                # total_price_subtotal_incl += line.price_subtotal_incl

                # YEAR
                sales_dict['year']['total'] += line.price_subtotal_incl
                # total_tax += 0

                # DAY
                if line.sh_pos_order_id.date_order.day == current_day:
                    sales_dict['day']['total'] += line.price_subtotal_incl

                # WEEK
                # if line.date_order.weekday == current_week:
                #     sales_dict['week']['total'] += line.price_subtotal_incl

                # MONTH
                if line.sh_pos_order_id.date_order.month == current_month:
                    sales_dict['month']['total'] += line.price_subtotal_incl

        for key in sales_dict:
            sales_dict[key]['total'] = '{:.2f}'.format(sales_dict[key]['total'])

        # payment_lines = self.env['sh.pos.payment'].sudo().search([
        #     ('sh_shop_id', '=', self.id)
        # ])

        # payment_lines = self.get_records_current_year('sh.pos.payment', 'date_order')
        # payment_dict = {}
        payment_day_dict = {}
        payment_week_dict = {}
        payment_month_dict = {}
        payment_year_dict = {}
        if payment_lines:
            for payment_line in payment_lines:

                # if payment_line.payment_method not in payment_dict:
                #     payment_dict[payment_line.payment_method] = 0.0
                # payment_dict[payment_line.payment_method] +=  payment_line.amount

                # YEAR
                if payment_line.payment_method not in payment_year_dict:
                    payment_year_dict[payment_line.payment_method] = 0.0
                payment_year_dict[payment_line.payment_method] +=  payment_line.amount

                # DAY
                if payment_line.sh_pos_order_id.date_order.day == current_day:
                    if payment_line.payment_method not in payment_day_dict:
                        payment_day_dict[payment_line.payment_method] = 0.0
                    payment_day_dict[payment_line.payment_method] +=  payment_line.amount

                # WEEK
                # if payment_line.date_order.weekday == current_week:
                    # if payment_line.payment_method not in payment_week_dict:
                    #     payment_week_dict[payment_line.payment_method] = 0.0
                #     payment_week_dict[payment_line.payment_method] +=  payment_line.amount

                # MONTH
                if payment_line.sh_pos_order_id.date_order.month == current_month:
                    if payment_line.payment_method not in payment_month_dict:
                        payment_month_dict[payment_line.payment_method] = 0.0
                    payment_month_dict[payment_line.payment_method] +=  payment_line.amount

        sales_dict['year']['payment_list'] = [{'name': key, 'value': '{:.2f}'.format(payment_year_dict[key])} for key in payment_year_dict]
        sales_dict['day']['payment_list'] = [{'name': key, 'value': '{:.2f}'.format(payment_day_dict[key])} for key in payment_day_dict]
        sales_dict['week']['payment_list'] = [{'name': key, 'value': '{:.2f}'.format(payment_week_dict[key])} for key in payment_week_dict]
        sales_dict['month']['payment_list'] = [{'name': key, 'value': '{:.2f}'.format(payment_month_dict[key])} for key in payment_month_dict]

        # dashboard_data_list = []
        # for title in ['Day', 'Current Week', 'Current Month', 'Current Year']:
        #     dashboard_data_list.append({
        #         'title': f"Sales for {title}",
        #         'payment_list': [{'name': key, 'value': '{:.2f}'.format(payment_dict[key])} for key in payment_dict],
        #         'total_price_subtotal_incl': '{:.2f}'.format(total_price_subtotal_incl),
        #         'total_tax': 00.00
        #     })
        return [value for value in sales_dict.values()]

    def _get_shop_data(self):
        shop_objs = self.env['sh.client.shop'].sudo().search([])
        if not shop_objs:
            return {}
        
        session_objs = self.env['sh.pos.session'].sudo().search([])
        # if not session_objs:
        #     return {}

        # if not self:
        #     self = shop_objs[0]

        # if not self:
        #     self = session_objs[0]
        shop_list=[]

        session_list = [{
            'id': session.id,
            'name': session.name,
        } for session in session_objs]

        return {
            'selected_shop_id': self.id,
            'shops': shop_list,
            'sessions': session_list,
            'dashboard_data_list': self._get_sales_data_list()
        }

    def _get_customer(self,data):
        if data.get('res_id'):
            partner = False
            if data.get('phone') not in ['',False, None]:
                partner = self.env['res.partner'].sudo().search([('phone','=',data.get('phone'))], limit=1)
            if not partner:
                partner = self.env['res.partner'].sudo().create(data)
            
            if partner:
                return partner.id
        else:
            return False

    def _get_session(self,data):
        if data.get('res_id'):
            session = False
            session = self.env['sh.pos.session'].sudo().search([('res_id','=',data.get('res_id'))], limit=1)
            if not session:
                session = self.env['sh.pos.session'].sudo().create(data)

            if session:
                return session.id
        else:
            return False

        