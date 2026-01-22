from odoo import models, fields, api


#FAMILIA
class GsieFamiliasEc(models.Model):
    _name = 'gsie.family'
    _inherit = ['mail.thread']
    _description = 'Familias EC'

    name = fields.Char(string='Código')
    code = fields.Char(string="Familia", required=True)
    padres_ids = fields.One2many('gsie.padres.ec', 'parent_id', string='Padres')
    partner_ids = fields.One2many('res.partner', 'family_id', string='Alumnos')
    suscripciones_ids = fields.One2many('sale.subscription', 'family_id', string='Suscripciones')
    plan_pago = fields.Char(string="Plan de pago")

    #@api.model
    #def create(self, vals):
    #    vals['name'] = self.env['ir.sequence'].next_by_code('gsie.family')
    #    return super(GsieFamily, self).create(vals)

#PADRES DE FAMILIA
class GsiePadresEc(models.Model):
    _name = 'gsie.padres.ec'
    _inherit = ['mail.thread']
    _description = 'Padres Gsie'

    name = fields.Char(string='Nombres', required=True)
    identidad = fields.Char(string="Identidad")
    phone = fields.Char(string="Teléfono")
    email= fields.Char(string="Email")
    genero = fields.Selection([
        ('f', 'Femenino'),
        ('m', 'Masculino')
    ], string='Género')
    parent_id = fields.Many2one('gsie.family', string='Familia')
