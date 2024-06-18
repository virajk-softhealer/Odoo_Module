# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import datetime
from odoo import http
from odoo.http import request
import json
import requests


class ShErpMasterController(http.Controller):

    def _status(self, status, message=False, data=False):
        dump_vals = {"status": status}
        if message:
            dump_vals["message"] = message
        if data:
            dump_vals.update(data)
        return http.Response(
            json.dumps(dump_vals),
            content_type='application/json;charset=utf-8',
            status=status
        )

    @http.route("/sh_erp_master/js", type='json', auth="public", methods=['GET', 'POST'], csrf=False)
    def sh_erp_master_js(self, **params):
        data = request.httprequest.data
        if not data:
            return []
        data = json.loads(data)
        if not data.get('params'):
            return []
        if not data['params'].get('shopId'):
            return []
        shop_id = data['params']['shopId']
        shop_obj = request.env['sh.client.shop'].sudo().search([
            ('id', '=', shop_id)
        ])
        if not shop_obj:
            return []

        # return shop_obj._get_shop_data()
        return {}


    @http.route("/sh_erp_master/<string:access_token>", type='http', auth="public", methods=['GET', 'POST'], csrf=False)
    def sh_erp_master(self, access_token, **params):
        data = request.httprequest.data
        # Validations
        if not data:
            return self._status(404, "Please provide the payloads !")
        data = json.loads(data)

        # -------------------------------------
        #  Check Shop
        shop_obj = request.env['sh.client.shop'].sudo().search([
            ('access_token', '=', access_token)
        ], limit=1)
        if not shop_obj:
            self._status(404, "shop_obj not found !")
            return self._status(404, "shop_obj not found !")

        response = shop_obj._process_shop_data(data)
        print("\n\n RESPONSE............",response)
        
        if not response:
            return self._status(404, "Please provide the payloads !")

        if response.get('error'):
            self._status(400, response['error'])

        return self._status(200, response.get('success'))

    # @http.route("/sh_saas_master/subscription/<string:uuid>", type='http', auth="public", methods=['GET'], csrf=False)
    # def client_user_creation(self, uuid=False):
    #     # -------------------------------------
    #     #  Check Subscription
    #     # -------------------------------------
    #     subscription = request.env['sh.saas.master'].sudo().search([
    #         ('client_subscription_id', '=', uuid)
    #     ])
    #     if not subscription:
    #         return http.Response(
    #             json.dumps({
    #                 'error': 'Please Provide A Valid Subscription ID...!'
    #             }),
    #             status=404,
    #             mimetype='application/json'
    #         )
    #     # -------------------------------------
    #     if not subscription.restrict_user_creation:
    #         subscription.active_users += 1
    #         return http.Response(
    #             # json.dumps(data),
    #             status=200,
    #             mimetype='application/json'
    #         )
    #     # -------------------------------------
    #     #  Get Current Active Users Count
    #     # -------------------------------------
    #     if not subscription.client_odoo_url:
    #         return http.Response(
    #             json.dumps({
    #                 'error': 'Something Went Wrong !'
    #             }),
    #             status=500,
    #             mimetype='application/json'
    #         )

    #     if not subscription.client_odoo_url[-1] == '/':
    #         subscription.client_odoo_url += '/'
    #     response = False
    #     try:
    #         response = requests.get(
    #             f'{subscription.client_odoo_url}sh_saas_client/user_count')
    #     except:
    #         return http.Response(
    #             json.dumps({
    #                 'error': 'Something Went Wrong !'
    #             }),
    #             status=500,
    #             mimetype='application/json'
    #         )
    #     if not response:
    #         return http.Response(
    #             json.dumps({
    #                 'error': 'Something Went Wrong !'
    #             }),
    #             status=500,
    #             mimetype='application/json'
    #         )
    #     if response.status_code != 200:
    #         return http.Response(
    #             json.dumps({
    #                 'error': 'Something Went Wrong !'
    #             }),
    #             status=500,
    #             mimetype='application/json'
    #         )
    #     json_data = response.json()
    #     if json_data and 'count' in json_data:
    #         subscription.active_users = json_data['count']
    #     # -------------------------------------
    #     #  Is Max Limit Crossed ?
    #     # -------------------------------------
    #     if subscription.active_users == subscription.max_allowed_users:
    #         return http.Response(
    #             json.dumps({
    #                 'error': f'You already reach your maximum user limit {subscription.active_users} !'
    #             }),
    #             status=404,
    #             mimetype='application/json'
    #         )

    #     subscription.active_users += 1
    #     return http.Response(
    #         status=200,
    #         mimetype='application/json'
    #     )
