# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import AccessError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    permitir_credito = fields.Boolean(string="Permitir Crédito", default=False)
    is_staff = fields.Boolean(string="Staff", default=False)
    pos_line_payment_ids = fields.One2many(
        'pos.order.line.payment',
        'partner_id',
        string="Compras POS",
    )
    
    def action_show_credit_agreement(self):
        """Abrir el wizard del contrato de crédito"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'credit.agreement.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_partner_id': self.id,
                'default_agreement_accepted': self.permitir_credito,
            },
        }

    def unlink(self):
        """Impedir borrar registros a usuarios con el grupo 'Permisos Gestión Académica (Restringido)'"""
        # Obtener el grupo restringido
        restricted_group = self.env.ref('gsie_english_castle_module.group_englishc_user', raise_if_not_found=False)
        
        # Verificar si el usuario actual tiene el grupo restringido
        if restricted_group and restricted_group in self.env.user.groups_id:
            raise AccessError(
                "No tiene permiso para eliminar registros de alumnos. "
                "Solo usuarios con permisos de administrador pueden eliminar registros."
            )
        
        return super().unlink()
