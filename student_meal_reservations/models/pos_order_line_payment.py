# -*- coding: utf-8 -*-
from odoo import models, fields, tools


class PosOrderLinePayment(models.Model):
    _name = 'pos.order.line.payment'
    _description = 'Líneas POS por Método de Pago'
    _auto = False
    _order = 'order_date desc'

    partner_id = fields.Many2one('res.partner', string='Cliente', readonly=True)
    order_id = fields.Many2one('pos.order', string='Orden', readonly=True)
    order_date = fields.Datetime(string='Fecha', readonly=True)
    product_id = fields.Many2one('product.product', string='Producto', readonly=True)
    qty = fields.Float(string='Cantidad', readonly=True)
    price_unit = fields.Float(string='Precio Unit.', readonly=True)
    price_subtotal_incl = fields.Float(string='Total', readonly=True)
    payment_method_id = fields.Many2one('pos.payment.method', string='Método de Pago', readonly=True)
    payment_amount = fields.Float(string='Monto Pago', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    (pol.id * 100000 + pp.id) AS id,
                    po.partner_id,
                    pol.order_id,
                    po.date_order AS order_date,
                    pol.product_id,
                    ROUND((pol.qty * pp.amount / NULLIF(po.amount_total, 0))::numeric, 2) AS qty,
                    pol.price_unit,
                    ROUND((pol.price_subtotal_incl * pp.amount / NULLIF(po.amount_total, 0))::numeric, 2) AS price_subtotal_incl,
                    pp.payment_method_id,
                    pp.amount AS payment_amount
                FROM pos_order_line pol
                JOIN pos_order po ON po.id = pol.order_id
                JOIN pos_payment pp ON pp.pos_order_id = po.id
                WHERE po.partner_id IS NOT NULL
                and po.state = 'done'
            )
        """ % self._table)
