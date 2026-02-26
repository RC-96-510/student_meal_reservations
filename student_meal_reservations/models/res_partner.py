# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import AccessError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    permitir_credito = fields.Boolean(string="Permitir Crédito", default=False)

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
