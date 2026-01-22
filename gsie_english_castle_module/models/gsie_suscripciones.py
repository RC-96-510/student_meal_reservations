# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

#HERENCIA NUEVOS CAMPOS A SUSCRIPCIONES
class GsieSuscripcionesec(models.Model):
    _inherit = 'sale.subscription'
    
    family_id = fields.Many2one("gsie.family", string="Código de Familia", related='partner_id.family_id', store=True)
    familia = fields.Char(string="Familia", related='partner_id.family_id.code', store=True)
    grado_id = fields.Many2one("gsie.grados", string="Grade level")

    @api.onchange('grado_id')
    def _onchange_grade_level(self):
       
        if self.partner_id:
            self.partner_id.grado_id = self.grado_id
    
    @api.depends('stage_id', 'partner_id')
    def _check_unique_subscription_in_progress_ec(self):
       
        for record in self:
            # Check if the stage category is 'progress'
            if record.stage_id.category == 'progress':
                # Find other subscriptions for the same partner with a 'progress' stage
                existing_subscriptions = self.search_count([
                    ('partner_id', '=', record.partner_id.id),
                    ('stage_id.category', '=', 'progress'),
                    ('id', '!=', record.id)
                ])
                if existing_subscriptions > 0:
                    raise UserError(
                        "El cliente {} ya tiene una suscripción en progreso. No puede crear otra, en su lugar cancele la suscripción anterior e inice la suscripción actual.".format(
                            record.partner_id.name
                        )
                    )
    
    def write(self, vals):
        # Ejecutamos la lógica cuando se actualiza el registro
        res = super(GsieSuscripcionesec, self).write(vals)

        # Verificamos si el stage_id ha cambiado
        if 'stage_id' in vals:
            if self.stage_id.category == 'progress':
                self.partner_id.state = 'enrolled'
            elif self.stage_id.category == 'closed':
                self.partner_id.state = 'no_matriculado'
        
        return res
