odoo.define('sh_erp_master.dashboard', function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var rpc = require('web.rpc');
    var session = require('web.session');
    var QWeb = core.qweb;
    var erp_master_details = [];
    var ERPMasterDashboardView = AbstractAction.extend({
        events: {
            'click #store_id': 'selectShopId',
            // 'change .edit-reason-for-clarification': 'saveReasonForClarification',
        },
        init: function (parent, context) {
            this._super(parent, context);
            var self = this;
            if (context.tag == 'erp_master_dashboard.dashboard') {
                self._rpc({
                    model: 'sh.erp.master.dashboard',
                    method: 'get_erp_master_dashboard_details',
                    args: ['123']
                }, []).then(function(result){
                    // erp_master_details = result
                    console.log("result: ", result)
                    self.render(result);
                })
            }
        },

        render: function (erp_master_details) {
            var super_render = this._super;
            var self = this;
            var erp_master_dashboard = QWeb.render(
                'erp_master_dashboard.dashboard',
                {
                    widget: self,
                    erp_data_dict: erp_master_details
                }
            );
            // $( ".o_control_panel" ).addClass( "o_hidden" );
            $(erp_master_dashboard).prependTo(self.$el);
            $("#store_id").click();
            return erp_master_dashboard
        },

        async selectShopId(event) {
            // alert("dsjkds ");
            var self = this;
            const select = $(event.currentTarget);
            const shopId = select.val()
            const selectedText = select.find('option:selected').text();
                await this._rpc({
                    route: '/sh_erp_master/js',
                    params: {'shopId': shopId},
                }).then(function (responseData) {
                    // alert(responseData)
                    // console.log("\n\n\n\n\n\n > responseData>>", $(".sh_nitin").html(responseData));
                    // console.log("\n\n\n\n\n\n > Custom Class>>", $(".sh_nitin").html("<h1>Jatin</h1>"));
                    // self.render(responseData);
                    console.log(responseData)
                    // $('#target-div').html(responseData.html);
                    var self = this;
                    var sales_data_tmpl = QWeb.render(
                        'sh_erp_master_dashboard.sales_data',
                        {
                            widget: self,
                            erp_data_dict: responseData
                        }
                    );
                    
                    console.log("\n\n\n\n\n\n > Custom Class>>", $(".sh_erp_data_dashboard").html(sales_data_tmpl));

                })
            // }
        },

    });
    core.action_registry.add('sh_erp_master.dashboard', ERPMasterDashboardView);
    return ERPMasterDashboardView
});