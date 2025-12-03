# student_meal_reservations/models/student.py

from odoo import models, fields

class Student(models.Model):
    _name = 'school.student'
    _description = 'Student Profile'

    name = fields.Char(string='Name', required=True)
    student_id = fields.Char(string='Student ID', required=True, unique=True)
    credit_balance = fields.Float(string='Credit Balance', default=0.0)
    #reservation_ids = fields.One2many('school.meal.reservation', 'student_id', string='Reservations')

