student_meal_reservations/
├── __manifest__.py
├── __init__.py
├── controllers/
│   └── student_menu.py              # Website controller for menu display
├── models/
│   ├── __init__.py
│   ├── student.py                   # Student model (with credit balance)
│   ├── meal.py                      # Meal model
│   ├── reservation.py               # Meal reservation model
│   └── topup.py                     # Credit top-up model
├── security/
│   ├── ir.model.access.csv          # Access control list
│   └── security.xml                 # Custom user groups
├── views/
│   ├── student_views.xml            # Backend form/tree views for students
│   ├── meal_views.xml               # Backend views for meals (admin & student)
│   ├── reservation_views.xml        # Backend views for reservations
│   ├── topup_views.xml              # Backend views for credit top-ups
│   └── website_templates.xml        # Website meal portal
└── static/                          # Optional: custom styling or JS
    └── description/
        └── icon.png                 # Module icon for Odoo Apps UI
