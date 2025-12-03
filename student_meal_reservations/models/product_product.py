# student_meal_reservations/models/student.py

from odoo import models, fields

class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    description = fields.Text("Description")
    ingredients = fields.Text("Ingredients")
    small_portion = fields.Text("Small portion")
    large_portion = fields.Text("Large portion")