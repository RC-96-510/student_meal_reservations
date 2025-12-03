from odoo import models, fields

class Menu(models.Model):
    _name = 'school.menu'
    _description = 'Menu'

    name = fields.Char(string='Name')
    date_from = fields.Date("Date from")
    date_to = fields.Date("Date to")
    state = fields.Selection([('Draft', 'Draft'),
                              ('Available', 'Available'),
                              ('Unavailable', 'Unavailable')], default='Draft')
    
    pdf_file = fields.Binary("Menu file")
    school_menu_detail_ids = fields.One2many("school.menu.detail", "school_menu_id", "Categories")

    def availableMenu(self):

        self.write({"state": "Available"})
    
    def UnavailableMenu(self):

        self.write({"state": "Unavailable"})
    
    def draftMenu(self):

        self.write({"state": "Draft"})

class MenuDetail(models.Model):
    _name = "school.menu.detail"
    _rec_name = "menu_category_id"

    day_of_the_week = fields.Selection([('Monday', 'Monday'),
                                 ('Tuesday', 'Tuesday'),
                                 ('Wednesday', 'Wednesday'),
                                 ('Thursday', 'Thursday'),
                                 ('Friday', 'Friday')], "Day of the week")
    
    menu_category_id = fields.Many2one("product.category", "Categoria")
    school_menu_id = fields.Many2one("school.menu", "school_menu_id")

    school_menu_detail_products_ids = fields.One2many("school.menu.detail.products", "school_menu_detail_id", "Products")

class MenuDetailProducts(models.Model):
    _name = "school.menu.detail.products"
    _rec_name = "product_id"

    product_id = fields.Many2one("product.product", "Product")
    small_portion_price = fields.Float("Small Portion Price (HNL)")
    large_portion_price = fields.Float("Large Portion Price (HNL)")
    
    school_menu_detail_id = fields.Many2one("school.menu.detail", "school_menu_detail_id")


