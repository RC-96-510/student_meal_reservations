# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class CreditAgreementWizard(models.TransientModel):
    _name = 'credit.agreement.wizard'
    _description = 'Credit Agreement Terms and Conditions'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    agreement_accepted = fields.Boolean(string='Accepted Agreement', default=False)

    def action_accept(self):
        """Accept the agreement and enable credit"""
        self.partner_id.permitir_credito = True
        return {
            'type': 'ir.actions.act_window_close'
        }

    def action_cancel(self):
        """Cancel the agreement and disable credit"""
        self.partner_id.permitir_credito = False
        return {
            'type': 'ir.actions.act_window_close'
        }
