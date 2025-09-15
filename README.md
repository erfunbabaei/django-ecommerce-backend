# Django E-commerce Backend

A full-featured backend for an e-commerce platform built with Django and Django REST Framework.  
This project provides APIs for user authentication, product management, order processing, shopping cart, and admin panel functionalities.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- **User Authentication**: Registration, login, password reset, and profile management.
- **Products**: CRUD operations for products with categories, stock management, and product images.
- **Shopping Cart**: Add, update, and remove products in the cart.
- **Orders**: Create orders from cart, track status, calculate total price, and manage stock.
- **Payments**: Track payment status and transaction IDs.
- **Admin Panel**: Manage users, products, orders, and payments.
- **Tests**: Comprehensive unit tests for models and key functionalities.

---

## Tech Stack
- **Backend**: Django 4.x, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Django default auth
- **Testing**: Django TestCase
- **Other Tools**: Git, GitHub

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/django-ecommerce-backend.git
   cd django-ecommerce-backend

2. Create a virtual environment and activate it:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate     # Windows

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Apply migrations:
    ```bash
    python manage.py migrate

5. Create a superuser for admin access:
    ```bash
    python manage.py createsuperuser

6. Run the development server:
    ```bash
    python manage.py runserver

## Configuration

- **Database:** Set PostgreSQL credentials in .env or settings.py.
- **Media Files:** Configure MEDIA_URL and MEDIA_ROOT in settings.py.
- **Environment Variables:** Use a .env file to store sensitive keys.

## Running Tests

- Run all tests with:
    ```bash
    python manage.py test

- Includes tests for users, products, orders, payments, and cart models.
- Ensures business logic like stock management, order total calculation, and payment status is working correctly.

## Project Structure

    django-ecommerce-backend/
    │
    ├─ users/           # User authentication and profile
    ├─ products/        # Product and ProductImage models
    ├─ orders/          # Cart, Order, OrderItem, Payment models
    ├─ admin_panel/     # Admin dashboard
    ├─ core/            # Project core settings and utils
    ├─ media/           # Uploaded product images
    ├─ static/          # Static files
    └─ manage.py

## Contributing

**Contributions are welcome!**
**Steps to contribute:**
1. Fork the repository
2. Create a new branch: git checkout -b feature/your-feature
3. Make your changes
4. Commit your work: git commit -m "Add feature"
5. Push to your branch: git push origin feature/your-feature
6. Open a Pull Request

