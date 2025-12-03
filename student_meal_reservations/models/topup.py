from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class CreditTopUp(models.Model):
    _name = 'student.credit.topup'
    _description = 'Student Credit Top-Up'
    _order = 'payment_date desc'

    student_id = fields.Many2one('school.student', string='Student', required=True)
    amount = fields.Float(string='Amount (HNL)', required=True)
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('done', 'Completed'),
        ('failed', 'Failed')
    ], default='pending', string='Payment Status')
    payment_date = fields.Datetime(string='Payment Date')
    transaction_id = fields.Char(string='Transaction ID', readonly=True)

    @api.model
    def mark_as_paid(self, transaction_id):
        """
        Mark a top-up as paid, typically called from a payment webhook or after manual validation.
        """
        topup = self.search([('transaction_id', '=', transaction_id)], limit=1)
        if not topup:
            raise ValidationError(f"No top-up found for transaction ID: {transaction_id}")
        if topup.payment_status == 'done':
            return topup  # Already processed

        topup.payment_status = 'done'
        topup.payment_date = datetime.now()

        # Add credit to the student's balance
        if topup.student_id:
            topup.student_id.credit_balance += topup.amount

        return topup

