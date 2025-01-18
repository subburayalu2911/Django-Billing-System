# Billing and Inventory Management System

This project is a simple Django-based billing and inventory management system. It allows users to manage products, generate bills for customers, calculate balance denominations, and send invoices via email in the background using Python's built-in threading library.

## Features

1. **Product Management**
   - CRUD operations for products: Name, Product ID, Available Stocks, Price per Unit, Tax Percentage.
   - CRUD operations for Denomination: Label, Count
   - Django REST framework panel available to manage products, customer, denomination.

2. **Billing Calculation**
   - Enter customer email and purchased items.
   - Dynamically add purchased products to the bill with quantity input.
   - Collect the paid amount.
   - Generate bill, display detailed calculations, and send the invoice to the customer's email asynchronously.
   - Calculate balance denominations to be given back based on shop availability.

3. **View Previous Purchases**
   - View all previous purchases by a customer.
   - View detailed information about a specific purchase, including purchased items.

## Assumptions

1. The available denominations are predefined as `[2000, 500, 200, 100, 50, 20, 10, 5, 2, 1]`.
2. Email configuration is set up using an SMTP server (can be updated in settings or environment variables).
3. The application is built to follow best practices and is production-ready.

## Tech Stack

- **Framework**: Django
- **Database**: SQLite (default, can be replaced with PostgreSQL or MySQL)
- **Frontend**: HTML with minimal CSS and JS
- **Asynchronous Task Queue**: Python's `threading` library for background tasks.
- **Email Delivery**: SMTP

## Setup Instructions

### Prerequisites

1. Python 3.8 or higher installed on your machine.
2. Clone the repository to your local machine.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/subburayalu2911/Django-Billing-System.git
    ```
2. Open the folder:
   ```
   cd Django-Billing-System
   ```
3. Create and activate a virtual environment:
   ```
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
   ````
4. Install dependencies:
    ```
    pip install -r requirements.txt
    ```    
5. Enter Email Credentials in Settings or Environment Variable:
     - Update the .env file with your email configuration for sending invoices:
       ```
        EMAIL_HOST=smtp.gmail.com
        EMAIL_PORT=587
        EMAIL_HOST_USER=your-email@gmail.com
        EMAIL_HOST_PASSWORD=your-email-password
        EMAIL_USE_TLS=True

6. Run migrations to set up the database:
   ```
     python manage.py makemigrations
     python manage.py migrate
   ```
7. Start the development server:
   ```
     python manage.py runserver
   ```

