# FoodPoint

FoodPoint is a Django web app for browsing dishes and managing simple food orders. It includes public pages (home, menu, contact), a reservation flow, an order tracking page, and a modern, responsive UI using Tailwind-style utility classes.

## Features

- Menu and dish browsing
- Add to cart, remove item from cart
- Modern quantity controls (+/−) with CSRF-safe AJAX calls
- Live line totals and cart summary updates
- Responsive UI using Tailwind CSS utility classes
- Reservation checkout flow (stub)
- Summary: Sticky card with auto-updating total

## Tech Stack

- Backend: Django
- Templates: Django Templates
- Styling: Tailwind CSS (utility classes)
- Runtime DB: SQLite (default)

## Getting Started

### Prerequisites

- Python 3.10+ (3.11 recommended)
- Git
- Node.js (only if you compile Tailwind locally; optional)

### Local Setup (Windows)

```powershell
# Clone
git clone https://github.com/huzaifa-asad/foodpoint-app-django.git
cd foodpoint

# Create and activate a virtualenv
py -3 -m venv .venv
.\.venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, create one:

```txt
Django>=4.2,<5.0
```

Then:

```powershell
pip install -r requirements.txt
```

### Database and Admin

```powershell
# Apply migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser
```

### Run the Dev Server

```powershell
python manage.py runserver
```

## Frontend Styling (Tailwind)

Templates use Tailwind classes. If you include Tailwind via CDN in your base template, nothing else is required. If you compile Tailwind locally, run your build script (example):

```powershell
# Example only, if you have a Tailwind build
npm install
npm run dev   # or: npm run build
```

## Cart: UX and Endpoints

The cart template uses data attributes and AJAX to sync quantities:

- Increase quantity: `POST /cart/increase/<dish_id>/`
- Decrease quantity: `POST /cart/decrease/<dish_id>/`
- Remove item: `GET /cart/remove/<dish_id>/` (navigates/redirects)
- Reservation (checkout): `GET /reservation/`

AJAX responses are JSON and include fields like:

```json
{
  "qty": 2,
  "line_total": 19.98,
  "cart": { "items": 3, "total": 54.47 }
}
```

The template adds the CSRF token via `X-CSRFToken` and updates:

- The quantity input
- The line total for the item
- The summary total

Key template: `core/templates/core/cart.html`  

- Uses Tailwind classes for modern styling
- Hooks: `data-item`, `data-qty`, `data-qty-input`, `data-line-total`
- Buttons: `data-action="inc"` and `data-action="dec"`
- Endpoints: `cart_increase`, `cart_decrease`, `cart_remove`

## Running Tests

If/when you add tests:

```powershell
python manage.py test
```

## Static Files (Production)

```powershell
# Collect static files into STATIC_ROOT
python manage.py collectstatic
```

Ensure your static files storage and web server are configured for production.

## Deployment Notes

- Set `DEBUG=False`
- Set `SECRET_KEY` and `ALLOWED_HOSTS`
- Configure a production database (e.g., Postgres) and cache if needed
- Serve static files (e.g., WhiteNoise, CDN) and media files
- Run migrations on deploy

## Git Conventions

- Branch: `feat/*`, `fix/*`, `chore/*`
- Commit message example:
  - `feat(cart): modernize cart UI and add +/- quantity controls with AJAX`

## License

MIT © 2025 huzaifa-asad. See [LICENSE](./LICENSE) for details.
