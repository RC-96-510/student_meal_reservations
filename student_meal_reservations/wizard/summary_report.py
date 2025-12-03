from odoo import models, fields, api
from odoo.exceptions import UserError

class SummaryReportWizard(models.TransientModel):
    _name = 'school.meal.summary.report'
    _rec_name = "registration_date"

    registration_date = fields.Date("Date from")
    date_to = fields.Date("Date to")

    school_meal_summary_report_detail_ids = fields.One2many("school.meal.summary.report.detail",
                                                            "school_meal_summary_report_id",
                                                            "school_meal_summary_report_detail_ids")

    def getInfo(self):

        self.env["school.meal.summary.report.detail"].search([('school_meal_summary_report_id', '=', self.id)]).unlink()
        
        obj_create = self.env["school.meal.summary.report.detail"]
        
        reservations = self.env["school.meal.reservation"].search([('state', '=', 'Confirmed'),
                                                                   ('reservation_date', ">=", self.registration_date),
                                                                   ('reservation_date', '<=', self.date_to)])

        for r in reservations:
            for r2 in r.school_meal_reservation_ids:
                for r3 in r2.school_meal_reservation_products_ids:

                 
                    bom = self.env["mrp.bom"].search([('product_id', '=', r3.product_id.product_id.id)])

                    for b in bom:
                        for b2 in b.bom_line_ids:

                            validated = self.env["school.meal.summary.report.detail"].search([('item', '=', b2.product_id.id),
                                                                                              ('school_meal_summary_report_id', '=', self.id)])
                            
                            if validated:
                                validated.qty += (b2.product_qty * r3.quantity)
                            
                            else:

                                vals = {
                                    'item': b2.product_id.id,
                                    'unit': b2.product_id.uom_id.id,
                                    'qty': b2.product_qty * r3.quantity,
                                    'price': b2.product_id.lst_price,
                                    'school_meal_summary_report_id': self.id
                                }

                                obj_create.create(vals)

class SummaryReportDetailWizard(models.TransientModel):
    _name = 'school.meal.summary.report.detail'

    item = fields.Many2one("product.product", "Item")
    unit = fields.Many2one("uom.uom", "Unit")
    qty = fields.Float("Quantity")
    price = fields.Float("Unit price")

    school_meal_summary_report_id = fields.Many2one("school.meal.summary.report", "school_meal_summary_report_id")





