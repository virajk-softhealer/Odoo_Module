/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, onMounted, useState, onWillUnmount } from "@odoo/owl";
import ajax from "web.ajax";
import { useBus, useService } from "@web/core/utils/hooks";
import { useOpenChat } from "@mail/views/open_chat_hook";
import core from "web.core";


export class ErpMasterDashboard extends Component {
  setup() {
    super.setup();

    alert('success fully got it')

    this.orm = useService('orm');
    this.rpc = useService('rpc');
    // useBus(this.env.bus, "sh_helpdesk_ticket_updated_notification", (ev) => this.initializeTimers());
    this.state = useState({
      // intervalIds: {},
      // selectedStepId: 0,
      // duration: 120000,
      // is_manager: false,
      // is_subordinate_employees:false,
      mailchannel: {
        'mail_channel_data': ''
      },
      // manager_dashboard_data: '',
      // total_dashboard_partners: '',
      // updatePartnerStatus: '',
      erp_data_dict: {}
    });


    this.busService = this.env.services.bus_service;

    onWillStart(this._onWillStart);
    // onWillUnmount(this._willUnmount);

    this.action = useService("action");
    this.messaging = useService("messaging");
    // this._handelNotification = this.handelNotification.bind(this)

  }

  _onWillStart() {
    this.initializeErpData()
    // this.busService.addEventListener(
    //   "notification",
    //   this._handelNotification
    // );
    // this.state.updatePartnerStatus = setInterval(() => {
    //   this.UpdatePartnerStatus();
    // }, 10000);

  }

  
  async initializeErpData() {
    const initialData = await this.orm.call(
      'sh.erp.master.dashboard',
      'get_erp_master_dashboard_details',
      [0]
    )
    console.log('====initialData=========>',initialData)
    this.state.erp_data_dict = initialData;
    // this.state.is_manager = initialData["is_manager"];
    // this.state.online_status = initialData["im_status"];
    // this.state.manager_dashboard_data = initialData["manager_dashboard_data"];
    // this.state.total_dashboard_partners = initialData["total_dashboard_partners"];
    // this.state.is_subordinate_employees = initialData["is_subordinate_employees"];

  }

}

ErpMasterDashboard.template = "erp_master_dashboard_template";
ErpMasterDashboard.components = {
  ...ErpMasterDashboard.components,
};
registry.category("actions").add("sh_erp_master.dashboard", ErpMasterDashboard);
