from odoo import models, fields, api
from odoo.exceptions import UserError

class StudentOrdersWizard(models.TransientModel):
    _name = 'school.meal.student.order'
    _rec_name = "student_id" 

    barcode = fields.Char("Student ID")
    student_id = fields.Many2one("res.partner", "Student")
    registration_date = fields.Date("Date", default=fields.Date.context_today)

    school_meal_student_order_detail_ids = fields.One2many("school.meal.student.order.detail", 
                                                           "school_meal_student_order_id",
                                                           "Orders")
    
    def getInfo(self):

        if not self.student_id:
            raise UserError("You must select a student")
        
        if not self.registration_date:
            raise UserError("You must select a date")

        
        reservations = self.env["school.meal.reservation.students"].search([('student_id', '=', self.student_id.id),
                                                                            ('state', '=', 'Confirmed')])


    
        if len(reservations) == 0:
            raise UserError("This student has no reservations")
        
        self.env["school.meal.student.order.detail"].search([('school_meal_student_order_id', '=', self.id)]).unlink()
        obj_create = self.env["school.meal.student.order.detail"]
         
        for r in reservations:

            lines = []

            for r2 in r.school_meal_reservation_products_ids:
                lines.append((0, 0, {
                    'category_id': r2.category_id.id,
                    'product_id': r2.product_id.id,
                    'size': r2.size,
                    'price': r2.price,
                    'quantity': r2.quantity,
                    'total': r2.total
                }))

            vals = {
                'order_id': r.id,
                'num_order': r.num_order,
                'student_id': r.student_id.id,
                'menu_id': r.menu_id.id,
                'total_pay': r.total_pay,
                'state': r.state,
                'school_meal_student_order_id': self.id,
                'school_meal_student_order_detail_products_ids': lines
            }

            obj_create.create(vals)


    @api.onchange("barcode")
    def getStudent(self):
       
        if self.barcode:
            
            student_id = self.env["res.partner"].search([('codigo_estudiante', '=', self.barcode)], limit=1)

            if not student_id:
                raise UserError("There is no student with the code: "+ str(self.barcode))
            
            self.student_id = student_id.id
            
class StudentOrdersDetailWizard(models.TransientModel):
    _name = 'school.meal.student.order.detail'

    num_order = fields.Char("Order Number")   
    order_id = fields.Many2one("school.meal.reservation.students", "Order")
    student_id = fields.Many2one("res.partner", "Student")
    menu_id = fields.Many2one("school.menu", "Menu")
    total_pay = fields.Float("Total pay")
    state = fields.Selection([('Draft', 'Draft'),
                              ('Confirmed', 'Confirmed'),
                              ('Paid', 'Paid'),
                              ('Delivered', 'Delivered'),
                              ('Cancelled', 'Cancelled')], default="Draft")

    school_meal_student_order_id = fields.Many2one("school.meal.student.order", "school_meal_student_order_id")
    school_meal_student_order_detail_products_ids = fields.One2many("school.meal.student.order.detail.products", 
                                                                    "school_meal_student_order_detail_id", "Products") 
    
    def setDelivered(self):

        self.write({'state':'Delivered'})
        self.order_id.state = 'Delivered'
        

class StudentOrdersDetailProductsWizard(models.TransientModel):
    _name = 'school.meal.student.order.detail.products'

    category_id = fields.Many2one("school.menu.detail", "Category")
    product_id = fields.Many2one("school.menu.detail.products", "Product")
    description = fields.Text("Description", related="product_id.product_id.description")
    ingredients = fields.Text("Ingredients", related="product_id.product_id.ingredients")
    portion = fields.Text("Portions", related="product_id.product_id.small_portion")
    size = fields.Selection([('Small', 'Small'),
                             ('Large', 'Large')], "Size")
    price = fields.Float("Price")
    quantity = fields.Integer("Quantity")
    total = fields.Float("Total pay")

    school_meal_student_order_detail_id = fields.Many2one("school.meal.student.order.detail", 
                                                          "school_meal_student_order_detail_id")





