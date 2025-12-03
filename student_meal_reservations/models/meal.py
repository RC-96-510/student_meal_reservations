# student_meal_reservations/models/meal.py

from odoo import models, fields

class Meal(models.Model):
    _name = 'school.meal'
    _description = 'Meal Item'

    name = fields.Char(string='Meal Name', required=True)
    meal_type = fields.Selection([
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch')
    ], string='Meal Type', required=True)
    date = fields.Date(string='Date', required=True)

    small_portion_price = fields.Float(string='Small Portion Price (HNL)')
    large_portion_price = fields.Float(string='Large Portion Price (HNL)')

    calories = fields.Integer(string='Calories')
    nutrition_tags = fields.Char(string='Nutrition Tags')
    allergens = fields.Char(string='Allergens')

    #reservation_ids = fields.One2many('school.meal.reservation', 'meal_id', string='Reservations')

