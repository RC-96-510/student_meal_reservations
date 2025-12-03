from odoo import http
from odoo.http import request

class StudentMealController(http.Controller):

    @http.route('/Elliots-Shack/menu', type='http', auth='user', website=True)
    def student_menu(self, **kwargs):
        menus = request.env['school.menu'].sudo().search([('state', '=', 'Draft')])
        print("Menus found:", menus)  # Depuración
        return request.render('student_meal_reservations.menu_page_template', {
            'menus': menus
        })

