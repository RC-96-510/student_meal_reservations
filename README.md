# 🥗 Student Meal Reservations – Odoo Module

An Odoo module for K–12 schools to manage daily meal menus and allow students to reserve meals using credits from their account.

---

## 📦 Features

- 📅 Admin management of breakfast and lunch menus by date
- 🍽️ Student meal reservation with portion size and nutrition info
- 💳 Student credit accounts with backend top-up tracking
- 🌐 Website portal to view meals (by logged-in students)
- 🔐 Group-based access: separate admin and student views

---

## 📂 Module Structure

student_meal_reservations/
├── controllers/
│ └── student_menu.py
├── models/
│ ├── student.py
│ ├── meal.py
│ ├── reservation.py
│ └── topup.py
├── security/
│ ├── ir.model.access.csv
│ └── security.xml
├── views/
│ ├── student_views.xml
│ ├── meal_views.xml
│ ├── reservation_views.xml
│ ├── topup_views.xml
│ └── website_templates.xml
├── init.py
└── manifest.py


---

## 🚀 Installation

1. Clone or copy the `student_meal_reservations` folder into your Odoo `addons` directory.
2. Restart the Odoo server.
3. Activate developer mode.
4. Install the module via Apps in the Odoo backend.

---

## 🌍 Access Points

- `/web` — Admin backend for managing meals, students, and top-ups
- `/elliots-shack/menu` — Student-facing website menu (requires login)

---

## 🛠️ Planned Extensions

- Stripe or local payment gateway integration for credit card top-ups
- Meal reservation via website with real-time balance deduction
- Weekly filters and student balance dashboard

---

## 📜 License

[LGPL-3](https://www.gnu.org/licenses/lgpl-3.0.html)

---

## 👨‍💻 Author

**Elliot’s Shack** – Powered by [english-castle.com](https://english-castle.com)
