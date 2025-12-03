# student_meal_reservations/models/student.py

from odoo import models, fields

class ProductCategoryInherit(models.Model):
    _inherit = 'product.category'

    is_menu_category = fields.Boolean("It is a menu category")