# -*- coding: utf-8 -*-
from odoo import models, fields

class GsieGraados(models.Model):
    _name = 'gsie.grados'
    _inherit = ['mail.thread']
    _description = 'Grados'
    
    name = fields.Char(string='Grado', required=True)
    category_id = fields.Many2one("product.category", string="Categoría")
    

