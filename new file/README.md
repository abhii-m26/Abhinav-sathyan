# Django E-Commerce App

Full-stack e-commerce demo built with Django templates, HTML, CSS, and JavaScript.

## Features

- Home, product listing, product detail, cart, checkout, login, sign up, and profile pages
- Product filters by category and price
- Dynamic cart updates through JavaScript and JSON endpoints
- User registration, login, logout, and profile management
- Django admin product CRUD
- REST-style JSON endpoints for products, cart, and orders
- SQLite database by default

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_products
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

Admin is available at `http://127.0.0.1:8000/admin/`.
