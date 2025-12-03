from odoo import models, fields

class GsieFamilyInherit(models.Model):
    _inherit = "gsie.family"

    related_user_id = fields.Many2one("res.users", "Usuario Odoo")

