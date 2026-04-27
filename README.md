# gym_activity_tracking_app

1.	How to effectively integrate React Native and Django to support online and offline operations, data storage, and frequent synchronisation with a server database in a tracking application?
2. HTTP protocols, data transfers, authentication, sensitive data encryption, SQL injections, how to prevent data breaches and secure users’ data?
3. Efective methods of testing modular applications to accelerate development and improve maintainability.


# Workout Tracker API

REST API for a personal workout-tracking application. Built with Django and Django REST Framework, using JWT for authentication and SQLite for local development. Companion clients in React (web) and React Native (Expo) consume this API.

## Features

- JWT authentication with access + refresh tokens and token blacklisting on logout
- Custom User model with UUID primary key
- Five domain apps: `users`, `exercises`, `plans`, `workouts`, plus a planned `progress` app
- Workout plan templates with nested days and exercises
- Workout logging with per-set reps, weight, and rest tracking
- Prefill endpoint that bridges plan templates and live workout logging
- Per-user data isolation enforced at the queryset layer
- Filtering on the exercise library (muscle group, equipment, compound/isolation)
- Test suite covering functional behaviour and security boundary

## Tech stack

- Python 3.10+ / Django 5
- Django REST Framework
- djangorestframework-simplejwt — JWT authentication
- drf-nested-routers — nested URL routing for plans → units → exercises
- SQLite (development) — drop-in replaceable with PostgreSQL via the `DATABASES` setting

## Project structure

```
backend/
├── workout_api/        # project settings, root URL conf
├── users/              # custom User model, auth endpoints
├── exercises/          # muscle groups, equipment types, exercise library
├── plans/              # workout plans, units (days), planned exercises
├── workouts/           # workouts, sets, prefill endpoint
├── manage.py
└── db.sqlite3
```

## Setup

```bash
# 1. Clone and enter the backend directory
cd backend

# 2. Create and activate a virtual environment
python -m venv env

# Windows
env\Scripts\activate

# macOS / Linux
source env/bin/activate

# 3. Install dependencies
pip install -r ./backend/dependecies.txt

# 4. Run migrations
python manage.py migrate

# 5. Seed the exercise library
python manage.py seed_exercises

# 6. Start the development server
python manage.py runserver
```

The API will be running at `http://127.0.0.1:8000/`.

### Optional — create an admin user for the Django admin

```bash
python manage.py createsuperuser
```

## Running the tests

```bash
# All apps
python manage.py test -v 2

# Single app
python manage.py test workouts -v 2

# Capture output to a log file (useful as a project artefact)
python manage.py test -v 2 > test_results.log 2>&1
```

## Authentication

All endpoints except `register`, `login`, and `refresh` require a JWT in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Tokens are issued on login. The access token is short-lived (1 day); when it expires, exchange the refresh token at `/api/auth/refresh/` for a new one. Logout blacklists the refresh token so it can no longer mint new access tokens.

## Endpoints

### Authentication

| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/api/auth/register/` | none | Create a user account |
| POST | `/api/auth/login/` | none | Issue access + refresh tokens |
| POST | `/api/auth/refresh/` | none | Get new access token |
| GET | `/api/auth/me/` | yes | Return authenticated user |
| POST | `/api/auth/logout/` | yes | Blacklist refresh token |

### Exercise library (read-only)

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/muscle-groups/` | List muscle groups |
| GET | `/api/equipment-types/` | List equipment types |
| GET | `/api/exercises/` | List exercises (supports filters) |
| GET | `/api/exercises/{id}/` | Retrieve one exercise |

Supported filters on `/api/exercises/`: `?muscle_group=<uuid>`, `?equipment_type=<uuid>`, `?is_compound=true|false`. Filters can be combined.

### Workout plans

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/plans/` | List the user's plans |
| POST | `/api/plans/` | Create a plan |
| GET | `/api/plans/{id}/` | Retrieve a plan with all nested days and exercises |
| PATCH | `/api/plans/{id}/` | Update a plan |
| DELETE | `/api/plans/{id}/` | Delete a plan (cascades) |
| POST | `/api/plans/{id}/units/` | Add a day to a plan |
| PATCH | `/api/plans/{id}/units/{u}/` | Edit a day |
| DELETE | `/api/plans/{id}/units/{u}/` | Delete a day |
| POST | `/api/plans/{id}/units/{u}/exercises/` | Add an exercise to a day |
| PATCH | `/api/plans/{id}/units/{u}/exercises/{e}/` | Edit a planned exercise |
| DELETE | `/api/plans/{id}/units/{u}/exercises/{e}/` | Remove a planned exercise |
| GET | `/api/plans/{id}/units/{u}/prefill/` | Plan defaults for autofill |

### Workouts

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/workouts/` | Start a workout |
| GET | `/api/workouts/` | Workout history (newest first) |
| GET | `/api/workouts/{id}/` | Retrieve a workout with all sets |
| PATCH | `/api/workouts/{id}/` | Mark complete, add notes |
| DELETE | `/api/workouts/{id}/` | Delete a workout (cascades to sets) |
| POST | `/api/workouts/{id}/sets/` | Log a set |
| PATCH | `/api/workouts/{id}/sets/{s}/` | Edit a set |
| DELETE | `/api/workouts/{id}/sets/{s}/` | Delete a set |

## Quickstart with HTTPie

The full happy path from registration through logging a set:

```bash
# Register
http POST :8000/api/auth/register/ \
  username=john email=john@test.com password=secret123

# Login (save the access token from the response)
http POST :8000/api/auth/login/ username=john password=secret123

export TOKEN="<paste access token here>"

# Browse the seeded exercise library
http GET :8000/api/exercises/ "Authorization: Bearer $TOKEN"

# Create a plan
http POST :8000/api/plans/ "Authorization: Bearer $TOKEN" \
  name="3 week hypertrophy" goal="muscle gain" length_weeks:=3

# Add a day to the plan (use the plan id from the previous response)
http POST :8000/api/plans/<plan_id>/units/ "Authorization: Bearer $TOKEN" \
  weekly_order:=1 name="Push day"

# Add an exercise to that day
http POST :8000/api/plans/<plan_id>/units/<unit_id>/exercises/ \
  "Authorization: Bearer $TOKEN" \
  exercise=<exercise_uuid> order_index:=1 default_sets:=4 \
  rep_range_min:=6 rep_range_max:=12 rest_seconds:=120

# Get prefill data for the day (drives the workout-logging form)
http GET :8000/api/plans/<plan_id>/units/<unit_id>/prefill/ \
  "Authorization: Bearer $TOKEN"

# Start a workout against that day
http POST :8000/api/workouts/ "Authorization: Bearer $TOKEN" \
  plan=<plan_uuid> workout_unit=<unit_uuid>

# Log a set
http POST :8000/api/workouts/<workout_id>/sets/ \
  "Authorization: Bearer $TOKEN" \
  exercise=<exercise_uuid> set_number:=1 reps:=10 \
  weight_kg=80.0 rest_after_seconds:=90

# Mark the workout complete
http PATCH :8000/api/workouts/<workout_id>/ \
  "Authorization: Bearer $TOKEN" \
  notes="felt strong"
```

> **HTTPie tip:** `:=` sends a number, `=` sends a string. So `set_number:=1` sends `1` (integer); `weight_kg=80.0` sends `"80.0"` (string), which DRF then coerces to a Decimal.

## Data model

```
User                ── owns ──>  WorkoutPlan
                                      └── has ──>  WorkoutUnit (a day)
                                                       └── has ──>  PlanExercise
                                                                         └── refs ──>  Exercise (library)

User                ── owns ──>  Workout
                                     ├── refs ──>  WorkoutPlan
                                     ├── refs ──>  WorkoutUnit
                                     └── has  ──>  Set
                                                      └── refs ──>  Exercise (library)

Exercise            ── belongs to ──>  MuscleGroup
                    ── belongs to ──>  EquipmentType (optional)
```

Key design decisions:

- **UUID primary keys everywhere.** Identifiers cannot be enumerated sequentially.
- **`Set.exercise` references the library exercise**, not the planned exercise. This means a user can log a set that wasn't in the plan without breaking referential integrity, and analytics queries (e.g. "best bench press ever") stay simple.
- **`on_delete=PROTECT` on plan/unit foreign keys from `Workout`.** A user cannot delete a plan that still has logged history, preserving the integrity of past sessions.
- **`on_delete=CASCADE` from `Workout` to `Set`.** Sets only exist in the context of their workout.
- **`unique_together` constraints** on `(plan, weekly_order)` and on `(workout, exercise, set_number)` prevent duplicate days within a plan and duplicate set numbers within a workout-exercise combination.

## Security

- **JWT authentication** issued and verified by `djangorestframework-simplejwt`. Refresh tokens are blacklisted on logout.
- **Password hashing** via Django's PBKDF2-SHA256 with per-user salt. Passwords are never returned in any response.
- **Per-user data isolation** at the queryset layer. Every viewset's `get_queryset()` filters by `self.request.user`; nested resources filter via parent joins like `unit__plan__user=request.user`.
- **404, not 403, on cross-user resource access.** Resource identifiers cannot be enumerated by probing.
- **Mass-assignment prevention.** Ownership fields (`user`, `plan`, `unit`) are injected server-side at save time from the URL or session, never from the request body.
- **SQL injection prevention** via parameterised queries through Django's ORM. A regression test submits a classic injection payload and asserts no rows leak.

## Configuration

JWT lifetimes are configured in `workout_api/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

For production, shorten the access-token lifetime (e.g. 15 minutes) so the window of risk after a token leak is small.

To switch from SQLite to PostgreSQL, change the `DATABASES` block in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'workout_db',
        'USER': 'postgres',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Install the driver: `pip install psycopg2-binary`. No other code changes are needed; the ORM abstracts the database engine.

## Limitations and future work

- **Progress / personal records** (`/api/progress/...`) is planned but not implemented in this iteration.
- **No rate limiting yet.** DRF throttling classes should be added on auth endpoints to mitigate credential-stuffing.
- **No pagination on list endpoints.** Fine for personal-scale data; for production add `DEFAULT_PAGINATION_CLASS` in DRF settings.
- **No password reset flow.**
- **Email is not verified** on registration.

## License

Educational project — submitted as part of a research assignment.
