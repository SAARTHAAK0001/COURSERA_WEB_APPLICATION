# Little Lemon — Table Booking & Menu API

A Django + Django REST Framework project for the Little Lemon restaurant.
It serves static HTML pages (home, menu, booking) and exposes a REST API
for managing menu items and table bookings, backed by MySQL.

## Features

- Django-rendered HTML pages (`/`, `/menu/`, `/booking/`)
- REST API for menu items and bookings (full CRUD)
- Token-based user registration and authentication
- MySQL as the primary database (SQLite fallback for local testing)
- Unit tests covering models and API endpoints
- Insomnia collection for manual API testing (`insomnia_collection.json`)

## Project layout

```
LittleLemon/
├── littlelemon/        # project settings, root urls
├── restaurant/         # app: models, serializers, views, urls, tests
├── templates/           # base.html, index.html, menu.html, book.html
├── static/css/          # style.css
├── requirements.txt
├── insomnia_collection.json
└── manage.py
```

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database. By default the project expects MySQL; set
   environment variables to match your local server:
   ```bash
   export DB_NAME=littlelemon
   export DB_USER=root
   export DB_PASSWORD=yourpassword
   export DB_HOST=127.0.0.1
   export DB_PORT=3306
   ```
   Create the database first: `CREATE DATABASE littlelemon;`

   To test quickly without MySQL, set `USE_SQLITE=True` instead — the
   project falls back to a local `db.sqlite3` file.

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (for `/admin/` and to seed test data):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the dev server:
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` for the site, `/admin/` for the admin
   panel.

## Running tests

```bash
python manage.py test restaurant
```

## API reference

All endpoints are namespaced under `/api/`.

| Method | Endpoint                  | Auth required | Description                     |
|--------|----------------------------|----------------|----------------------------------|
| POST   | `/api/auth/register/`      | No             | Create a new user account        |
| POST   | `/api/auth-token/`         | No             | Exchange username/password for a token |
| GET    | `/api/menu-items/`         | No             | List menu items                  |
| POST   | `/api/menu-items/`         | Yes            | Create a menu item               |
| GET    | `/api/menu-items/<id>/`    | No             | Retrieve one menu item           |
| PUT    | `/api/menu-items/<id>/`    | Yes            | Replace a menu item              |
| PATCH  | `/api/menu-items/<id>/`    | Yes            | Partially update a menu item     |
| DELETE | `/api/menu-items/<id>/`    | Yes            | Delete a menu item               |
| GET    | `/api/bookings/`           | Yes            | List the current user's bookings |
| POST   | `/api/bookings/`           | Yes            | Create a booking                 |
| GET    | `/api/bookings/<id>/`      | Yes            | Retrieve one of your bookings    |
| PUT    | `/api/bookings/<id>/`      | Yes            | Replace a booking                |
| PATCH  | `/api/bookings/<id>/`      | Yes            | Partially update a booking       |
| DELETE | `/api/bookings/<id>/`      | Yes            | Delete a booking                 |

Authenticated requests use token auth:
```
Authorization: Token <your-token>
```

### Example flow (curl)

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -d "username=marioR&email=mario@example.com&password=SuperSecret123"

# Get a token
curl -X POST http://127.0.0.1:8000/api/auth-token/ \
  -d "username=marioR&password=SuperSecret123"

# Create a booking (replace TOKEN)
curl -X POST http://127.0.0.1:8000/api/bookings/ \
  -H "Authorization: Token TOKEN" \
  -d "name=Mario Rossi&no_of_guests=4&booking_date=2026-12-24&booking_time=19:30:00"
```

## Testing with Insomnia

Import `insomnia_collection.json` into Insomnia (**Create > Import > From File**).
It includes requests for registration, token auth, and full CRUD on menu
items and bookings, using `{{ _.base_url }}` and `{{ _.token }}` variables
you can set in the included environment.

## Git

```bash
git init
git add .
git commit -m "Initial commit: Little Lemon booking API"
git remote add origin <your-repo-url>
git push -u origin main
```
