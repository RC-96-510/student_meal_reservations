# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    citizenship = fields.Char(string='Nacionalidad')
    birthdate = fields.Date(string='Cumpleaños')
    genero = fields.Selection([
        ('male', 'Masculino'),
        ('female', 'Femenino')
    ], string='Género')
    codigo_estudiante = fields.Char(string='Código de estudiante')
    grado_id = fields.Many2one("gsie.grados", string='Nivel Académico')
    placement = fields.Char(string='Ubicación')
    state = fields.Selection([('enrolled', 'Inscrito'),('withdrawn', 'Retirado'), ('no_matriculado', 'No matriculado')], string='Estado')
    family_id = fields.Many2one("gsie.family", string="Familia")
    subscription_ids = fields.One2many('sale.subscription', 'partner_id', string="Suscripciones")  # Relación inversa
    category_id = fields.Many2one("product.category", string="Categoría", related="grado_id.category_id")
    es_alumno = fields.Boolean(string="Alumno")
    permitir_credito = fields.Boolean(string="Permitir Crédito")
    
    def action_retirar(self):
        # Cambiar el estado del partner a 'withdraw'
        subscription = self.env['sale.subscription'].search([
            ('partner_id', '=', self.id),
            ('stage_id.category', '=', 'progress')
        ], limit=1)

        if subscription:
            # Si hay una suscripción activa en progreso, no permitir cambiar el estado
            raise UserError("No se puede retirar el alumno hasta que se cierre la suscripción que tiene abierta.")
        
        # Si no hay suscripción en progreso, cambiar el estado del partner a 'withdraw'
        self.state = 'withdrawn'
        
        