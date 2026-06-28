# AI Agent Instructions

## Project overview
- Backend is a Django 6 REST API using Django REST Framework and Simple JWT.
- Auth is phone-number based with `AccountType` and OTP flows in `apps.accounts`.
- Customers have profile/address endpoints in `apps.customers`.
- The code uses a service layer (`services`), DTO validation with Pydantic (`dto`), and class-based API views (`APIView`).
- Custom user model: `AUTH_USER_MODEL = "accounts.User"`.

## Important files
- `pyproject.toml` — project dependencies and Python version
- `.pre-commit-config.yaml` — repo formatting/lint hooks using `ruff`
- `manage.py` — Django CLI entrypoint
- `config/settings.py` — env var based settings, DB defaults, JWT setup
- `config/urls.py` — root URL routing
- `apps/accounts/` — auth flow, user model, OTP integration
- `apps/customers/` — customer profile and addresses
- `utils/models.py` — shared abstract models for UUID primary keys and audit timestamps

## Tooling and conventions
- Use `python -m pip install -e .` or equivalent to install dependencies from `pyproject.toml`.
- Environment variables are loaded via `dotenv` in `config/settings.py`.
- Follow `ruff` for formatting and linting; run `pre-commit install` and `pre-commit run --all-files`.
- Prefer existing service and DTO patterns over introducing new architectural styles.
- Use Django management commands for migrations and runtime: `python manage.py migrate`, `python manage.py runserver`, `python manage.py test`.

## API and auth patterns
- `apps/accounts` exposes `/customer/auth/...` and `/seller/auth/...` endpoints.
- Auth flow is split into start, password login, and OTP verification.
- JWT payload includes `account_type`.
- Customer endpoints are protected with `IsAuthenticated` and `IsCustomer` permission checks.
- `UUIDPrimaryKey` and timestamp tracking are used across models.

## Agent guidance
- Avoid guessing app structure; use the concrete folder layout and naming conventions.
- Maintain current patterns around `APIView`, `Response`, DTO validation, and service methods.
- Do not add frontend or unrelated services; this repo is backend-only.
- Keep changes simple and aligned with Django/DRF idioms already present.
