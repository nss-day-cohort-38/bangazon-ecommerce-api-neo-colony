# Bangazon Django App Project Setup

1. Clone down the repo and `cd` into it
1. Set up your virtual environment:
    `python -m venv bangazonEnv`
1. Activate virtual environment:
    `source ./bangazonEnv/bin/activate`
1. Install dependencies:
    `pip install -r requirements.txt`
1. Run migrations:
    `python manage.py migrate`
1. `python manage.py runserver`
1. Create your application for your API, named `ecommerceapi`

# Install Safe Delete
1. Install Django Safe Delete using pip:
    `pip install django-safedelete`
1. Add `safedelete` in your `INSTALLED_APPS` in the admin app's `settings.py` file.
1. Run `python manage.py makemigrations` & `python manage.py migrate` to update your DB with the new safedelete module.

## ERD
Here is your [Bangazon eCommerce ERD](https://dbdiagram.io/d/5ed15c7b39d18f5553fff82c). There should be no changes made to your ERD without approval from your product manager.
