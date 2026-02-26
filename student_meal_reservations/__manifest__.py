{
    'name': "Student Meal Reservations",
    'version': '1.0',
    'summary': 'School meal reservation system with student credit management',
    'description': """
        Manage school meal menus and allow students to reserve meals using their credit balance.
        Includes backend admin tools and a student-facing website portal.
    """,
    'author': "Elliot's Shack",
    'website': "https://english-castle.com",
    'category': 'Education',
    'license': 'LGPL-3',
    'depends': ['base', 'stock', 'gsie_english_castle_module'],
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',

        # Views - backend
        'reports/student_id.xml',
        'reports/back_side_student_id.xml',
        'reports/student_id_contact.xml',
        'reports/back_side_student_id_contact.xml',
        'reports/token_id.xml',
        'reports/back_side_token_id.xml',
        'wizard/summary_report.xml',
        'wizard/student_orders.xml',
        'views/student_views.xml',
        'views/meal_views.xml',
        'views/reservation_views.xml',
        'views/menu_views.xml',
        'views/product_category.xml',
        'views/product_product.xml',
        'views/gsie_family.xml',
        'views/res_partner_view.xml',
        'views/menu.xml',
        #'views/topup_views.xml',            # ⬅️ NEW: admin credit top-ups

        # Views - website
        # 'views/website_templates.xml',      # student-facing meal portal

        # Menus and actions defined in views
    ],
    'installable': True,
    'application': True,
}

