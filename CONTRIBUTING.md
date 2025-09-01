# Contributing to FoodPoint

Thanks for your interest in contributing. This project is a Django app with templates, static assets, and simple views.

## Code of Conduct

Be respectful and constructive. Harassment or discrimination is not tolerated.

## How to Contribute

1. Open an issue to discuss changes.
2. Create a feature branch from main:
   - feat/`short-name`, fix/`short-name`, chore/`short-name`
3. Commit with Conventional Commits (see below).
4. Open a Pull Request (PR) with a clear description and screenshots for UI changes.

## Development Setup (Windows)

Prerequisites: Python 3.10+, Git

```powershell
# Clone
git clone https://github.com/huzaifa-asad/foodpoint-app-django.git
cd foodpoint

# Virtual environment
py -3 -m venv .venv
.\.venv\Scripts\activate

# Install deps
pip install -r requirements.txt
# If missing, minimally: pip install "Django>=4.2,<5.0"

# Migrate and (optional) seed demo data
python manage.py migrate
python manage.py seed_dishes

# Run
python manage.py runserver
```

## Running Tests

```powershell
python manage.py test
```

## Style Guide

- Python: PEP 8; prefer type hints where reasonable.
- Templates: Keep semantic HTML; use existing Tailwind utility patterns for consistency.
- JavaScript: Keep it small and framework-free unless discussed; prefer fetch and data-attributes.
- Formatting (optional but recommended):
  - Black and Ruff
  
    ```powershell
    pip install black ruff
    ruff check .
    black .
    ```

- Do not commit local artifacts:
  - Do not commit changes to db.sqlite3
  - Do not commit environment files (.env) or IDE settings

## Commit Messages (Conventional Commits)

- feat(cart): add +/- quantity controls with AJAX
- fix(menu): correct price formatting
- chore(ci): add GitHub Actions workflow

Types: feat, fix, docs, style, refactor, perf, test, build, chore

## Pull Request Checklist

- Branch created from main
- Meaningful title and description
- Tests updated/added if applicable
- No db.sqlite3 changes
- Lint/format run locally
- Screenshots/GIFs for UI changes
- Docs updated (README/inline docs) if behavior changes

## Issues

- Use clear titles and steps to reproduce.
- Label appropriately (bug, enhancement, docs).

## License

By contributing, you agree your contributions are licensed under the repository’s MIT License (c) 2025 huzaifa-asad.
