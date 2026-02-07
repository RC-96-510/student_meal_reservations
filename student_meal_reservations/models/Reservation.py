# student_meal_reservations/models/reservation.py

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime #This was added for topup functionality
import mimetypes
import base64

class MealReservation(models.Model):
    _name = 'school.meal.reservation'
    _description = 'Meal Reservation'
    _rec_name = "parent_id"
    _inherit = ['mail.thread']

    @api.depends("school_meal_reservation_ids.total_pay")
    def getTotalPay(self):
        total = 0

        for r in self.school_meal_reservation_ids:
            total += r.total_pay
        
        self.total_pay = total

    num_reservation = fields.Char("Reservation Number")
    parent_id = fields.Many2one("res.users", "User", default=lambda self: self.env.user, tracking=True)
    family_id = fields.Many2one("gsie.family", "Family", tracking=True)
    reservation_date = fields.Date("Reservation date", tracking=True)
    total_pay = fields.Float("Total pay", compute=getTotalPay, store=True, tracking=True)
    state = fields.Selection([('Draft', 'Draft'),
                              ('Confirmed', 'Confirmed'),
                              ('Paid', 'Paid'),
                              ('Cancelled', 'Cancelled')], default="Draft", tracking=True)
    
    school_meal_reservation_ids = fields.One2many("school.meal.reservation.students", 
                                                  "school_meal_reservation_id", 
                                                  "Students")
    @api.model
    def create(self, vals):
        record = super().create(vals)
        # Ahora sí el registro tiene ID y puedes usar message_post
        record.post_receipts_in_chatter()
        
        return record
    

    def post_receipts_in_chatter(self):
        """Adjunta todos los PDFs e imágenes relacionados de school.menu en el chatter de cada reserva."""
        
        for reservation in self:
            
            menus = self.env['school.menu'].search([('state', '=', 'Available')])
            if not menus:
                continue  

            attachment_ids = []

            for menu in menus:
                if menu.pdf_file:
                    # Detectar el tipo MIME del archivo automáticamente
                    file_name = menu.name
                    
                    # Intentar detectar el tipo MIME por extensión
                    mime_type, _ = mimetypes.guess_type(file_name)
                    
                    # Si no se detecta, usar un tipo por defecto según la extensión
                    if not mime_type:
                        if file_name.lower().endswith(('.pdf',)):
                            mime_type = 'application/pdf'
                        elif file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                            mime_type = 'image/png'  # Se ajustará automáticamente
                        else:
                            mime_type = 'application/octet-stream'
                    
                    attachment = self.env['ir.attachment'].create({
                        'name': file_name,
                        'type': 'binary',
                        'datas': menu.pdf_file,  # ya en base64
                        'res_model': reservation._name,
                        'res_id': reservation.id,
                        'mimetype': mime_type,
                    })
                    attachment_ids.append(attachment.id)

            if attachment_ids:
                reservation.message_post(
                    body="Available Menus",
                    attachment_ids=attachment_ids,
                )
    
    @api.onchange("parent_id")
    def getFamily(self):
    
        if self.parent_id:
            family = self.env["gsie.family"].search([('related_user_id', '=', self.parent_id.id)])

            if not family:
                raise UserError("This user has no related family")
            else:
                self.family_id = family.id
        
        

    def confirmOrder(self):
        
        for r in self.school_meal_reservation_ids:
            r.state = 'Confirmed'
            r.num_order = "Order#"+ str(r.id)
        
        self.write({'state':'Confirmed'})
        self.num_reservation = "Reservation#"+ str(self.id)

    def draftOrder(self):

        for r in self.school_meal_reservation_ids:
            r.state = 'Draft'
        
        self.write({'state':'Draft'})

    def cancelOrder(self):
        for r in self.school_meal_reservation_ids:
            r.state = 'Cancelled'
        
        self.write({'state':'Cancelled'})


class MealReservationStudent(models.Model):
    _name = 'school.meal.reservation.students'
    _rec_name = "num_order"

    @api.depends("school_meal_reservation_products_ids.total")
    def getTotalPay(self):
        self.total_pay = sum(r.total for r in self.school_meal_reservation_products_ids)


    @api.depends('school_meal_reservation_id.reservation_date')
    def _compute_day_name(self):
        for record in self:
            for r in record.school_meal_reservation_id:
                if r.reservation_date:
                    date_obj = fields.Date.from_string(r.reservation_date)
                    record.day_name = date_obj.strftime("%A")
                    
                else:
                    record.day_name = False
    
    @api.onchange("student_id")
    def validatedStudent(self):

        count = 0
        if self.student_id:

            for r in self.school_meal_reservation_id.school_meal_reservation_ids:
                if r.student_id.id == self.student_id.id:
                    count += 1
            
            if count > 1:
                raise UserError("The student "+str(self.student_id.name) +" has already been added to this reservation.")
        
    num_order = fields.Char("Order Number")    
    student_id = fields.Many2one("res.partner", "Student")
    menu_id = fields.Many2one("school.menu", "Menu")
    total_pay = fields.Float("Total pay", compute=getTotalPay, store=True)
    day_name = fields.Char("Day name", compute=_compute_day_name)
    state = fields.Selection([('Draft', 'Draft'),
                              ('Confirmed', 'Confirmed'),
                              ('Paid', 'Paid'),
                              ('Delivered', 'Delivered'),
                              ('Cancelled', 'Cancelled')], default="Draft")

    school_meal_reservation_id = fields.Many2one("school.meal.reservation", "school_meal_reservation_id")
    school_meal_reservation_products_ids = fields.One2many("school.meal.reservation.products", "school_meal_reservation_students_id", "Products") 

    @api.onchange("menu_id")
    def validateDate(self):
       
        if self.menu_id and self.school_meal_reservation_id.reservation_date:

            if self.school_meal_reservation_id.reservation_date < self.menu_id.date_from:
                raise UserError("This menu is only available from "+ str(self.menu_id.date_from) + " to "+ str(self.menu_id.date_to))
            
            if self.school_meal_reservation_id.reservation_date > self.menu_id.date_to:
                raise UserError("This menu is only available from "+ str(self.menu_id.date_from) + " to "+ str(self.menu_id.date_to))

class MealReservationProducts(models.Model):
    _name = 'school.meal.reservation.products'

    category_id = fields.Many2one("school.menu.detail", "Category")
    product_id = fields.Many2one("school.menu.detail.products", "Product")
    description = fields.Text("Description", related="product_id.product_id.description")
    ingredients = fields.Text("Ingredients", related="product_id.product_id.ingredients")
    portion = fields.Text("Portions", related="product_id.product_id.small_portion")
    size = fields.Selection([('Small', 'Small'),
                             ('Large', 'Large')], "Size")
    price = fields.Float("Price")
    quantity = fields.Integer("Quantity", default=1)
    total = fields.Float("Total pay")

    school_meal_reservation_students_id = fields.Many2one("school.meal.reservation.students", "school_meal_reservation_students_id")

    @api.onchange("product_id", "size")
    def getPrice(self):

        count = 0
        if self.product_id:

            for r in self.school_meal_reservation_students_id.school_meal_reservation_products_ids:
                if r.product_id.id == self.product_id.id:
                    count += 1
            
            if count > 2:
                raise UserError("The product "+str(r.product_id.product_id.name) +" has already been added to this order.")
        
        if self.product_id and self.size:
            if self.size == 'Small':
                self.price = self.product_id.small_portion_price
            
            if self.size == 'Large':
                self.price = self.product_id.large_portion_price
        

    
    @api.onchange("price", "quantity")
    def getTotal(self):

        self.total = self.price * self.quantity

