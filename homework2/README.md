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

# 5. create admin account (optional)
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

## Deployment (Render)

The app is deployed at: https://cs5300.onrender.com

### How to Deploy on Render

1. Push code to GitHub
2. Go to [render.com](https://render.com) and sign in with GitHub
3. Click **New** → **Web Service**
4. Select your GitHub repository
5. Configure:
   - **Language**: Python 3
   - **Root Directory**: `homework2`
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py seed_data`
   - **Start Command**: `gunicorn movie_theater_booking.wsgi:application`
   - **Instance Type**: Free
6. Add Environment Variables:
   - `SECRET_KEY` = your secret key
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `*`
   - `DISABLE_FORCE_SCRIPT` = `1`
7. Click **Deploy Web Service**

### Demo Credentials
- Username: `demo`
- Password: `demo1234`

---


