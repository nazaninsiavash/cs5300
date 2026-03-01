# Movie Theater Booking App (HW2)

Django REST API + UI for booking movie seats. Built for the intro Django assignment.

---

## What it does

- Browse movies and see how many seats are left
- Pick a seat and book it (login required)
- View / cancel your bookings
- Full REST API at `/api/`

---

## Project layout

```
homework2/
├── movie_theater_booking/   # project settings, urls, wsgi
├── bookings/
│   ├── models.py            # Movie, Seat, Booking
│   ├── views.py             # viewsets + template views
│   ├── serializers.py
│   ├── tests.py             # 65 tests (unit + parametrized)
│   ├── admin.py
│   ├── migrations/
│   ├── templates/bookings/  # html templates
│   ├── management/commands/
│   │   └── seed_data.py     # adds sample movies + demo user
│   └── features/            # BDD tests (behave)
├── manage.py
├── requirements.txt
├── Procfile
└── render.yaml
```

---

## How to run it

```bash
# 1. set up virtual env
python3 -m venv hw2 --system-site-packages
source hw2/bin/activate

# 2. install deps
cd ./cs5300/homework2
pip install -r requirements.txt

# 3. migrate
python manage.py makemigrations
python manage.py migrate

# 4. add sample data (extra)
python manage.py seed_data
# adds 4 movies with 40 seats each + demo user: demo / demo1234

# 5. create admin account
python manage.py createsuperuser

# 6. run
python manage.py runserver 0.0.0.0:3000
```

---

## API endpoints

| Method | URL | Notes |
|--------|-----|-------|
| GET | `/api/movies/` | list all movies |
| POST | `/api/movies/` | create (auth required) |
| GET | `/api/movies/<id>/seats/` | seats for a movie |
| GET | `/api/seats/?movie=<id>` | filter seats by movie |
| GET | `/api/seats/available/` | only free seats |
| GET | `/api/bookings/` | your bookings (auth) |
| POST | `/api/bookings/` | book a seat (auth) |
| DELETE | `/api/bookings/<id>/` | cancel a booking |

---

## Running tests

```bash
python manage.py test bookings

# with coverage
pip install coverage
coverage run manage.py test bookings
#app's coverage without Django internals, run:
coverage report --include="bookings/*,movie_theater_booking/*,manage.py"

```

## BDD tests

```bash
pip install behave behave-django --break-system-packages
pip install behave behave-django
python manage.py behave
```

---

## Deploying to Render

1. Push to GitHub
2. Go to render.com → New Web Service → connect repo
3. It'll pick up `render.yaml` automatically
4. Set a `SECRET_KEY` env var
5. Done!  build command runs migrations + seed automatically

---


