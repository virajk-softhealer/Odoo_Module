# -*- coding: utf-8 -*-
# Part of Softhealer Technologies


from odoo import api,models,fields, _ 

class PosOrder(models.Model):
    _inherit = "pos.order"

    # IR.ACTION.SERVER METHOD 

    def action_deduction_category_wise(self):

        self.env.cr.execute("""
            SELECT 
                COALESCE(pc.name->>'en_US', 'Unknown Category') AS category_name,
                COALESCE(ppm.name->>'en_US', 'Unknown Payment Method') AS payment_method_name,
                SUM(
                    CASE WHEN ppm.name->>'en_US' ILIKE 'CASH' 
                        THEN 
                            pol.price_subtotal_incl - (pol.price_subtotal_incl * pc.sh_deduct_percentage) 
                        ELSE 
                            pol.price_subtotal_incl 
                    END
                ) AS total_amounts,

                COALESCE(
                    SUM(
                        CASE WHEN ppm.name->>'en_US' ILIKE 'CASH' 
                            THEN 
                                pol.price_subtotal_incl - (pol.price_subtotal_incl * pc.sh_deduct_percentage) 
                            ELSE 
                                pol.price_subtotal_incl 
                        END
                    ) FILTER (WHERE po.date_order::date = CURRENT_DATE), 
                    0
                ) AS today_total_amount,

                COALESCE(
                    SUM(
                        CASE WHEN ppm.name->>'en_US' ILIKE 'CASH' 
                            THEN 
                                pol.price_subtotal_incl - (pol.price_subtotal_incl * pc.sh_deduct_percentage) 
                            ELSE 
                                pol.price_subtotal_incl 
                        END
                    ) FILTER (WHERE po.date_order >= date_trunc('week', CURRENT_DATE)), 
                    0
                ) AS weekly_total_amount,

                COALESCE(
                    SUM(
                        CASE WHEN ppm.name->>'en_US' ILIKE 'CASH' 
                            THEN 
                                pol.price_subtotal_incl - (pol.price_subtotal_incl * pc.sh_deduct_percentage) 
                            ELSE 
                                pol.price_subtotal_incl 
                        END
                    ) FILTER (WHERE po.date_order >= date_trunc('month', CURRENT_DATE)), 
                    0
                ) AS monthly_total_amount,

                COALESCE(
                    SUM(
                        CASE WHEN ppm.name->>'en_US' ILIKE 'CASH' 
                            THEN 
                                pol.price_subtotal_incl - (pol.price_subtotal_incl * pc.sh_deduct_percentage) 
                            ELSE 
                                pol.price_subtotal_incl 
                        END
                    ) FILTER (WHERE EXTRACT(YEAR FROM po.date_order) = EXTRACT(YEAR FROM CURRENT_DATE)), 
                    0
                ) AS yearly_total_amount

            FROM 
                pos_order_line pol
                JOIN pos_order po ON po.id = pol.order_id
                JOIN pos_payment pp ON po.id = pp.pos_order_id
                JOIN pos_payment_method ppm ON ppm.id = pp.payment_method_id
                JOIN product_product product_p ON product_p.id = pol.product_id
                JOIN product_template pt ON pt.id = product_p.product_tmpl_id
                JOIN pos_category pc ON pc.id = pt.pos_categ_id

            GROUP BY 
                category_name, payment_method_name;

        """)
        

        result = self.env.cr.dictfetchall()
        # print('\n\n\n\n RESULT',result) 

