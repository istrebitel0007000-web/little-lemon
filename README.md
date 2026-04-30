# Little Lemon

Django web app + REST API for the Little Lemon restaurant. PWA-ready (installable on Android via PWABuilder).

## Features

- Restaurant homepage, about, menu, booking pages
- User registration + login/logout
- Booking creation with confirmation email (console backend in dev)
- Menu search
- REST API (`/api/`) with JWT auth for `Booking` and `Menu`
- Installable PWA (manifest + service worker)

## Quick start

```bash
cd littlelemon
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt

copy .env.example .env         # Windows
# cp .env.example .env         # macOS / Linux

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## REST API

| Endpoint                   | Method      | Description                |
|----------------------------|-------------|----------------------------|
| `/api/token/`              | POST        | Get JWT access + refresh   |
| `/api/token/refresh/`      | POST        | Refresh JWT access token   |
| `/api/menu/`               | GET, POST   | List / create menu items   |
| `/api/menu/<id>/`          | GET/PUT/DEL | Menu detail                |
| `/api/bookings/`           | GET, POST   | List / create bookings     |
| `/api/bookings/<id>/`      | GET/PUT/DEL | Booking detail             |
| `/api/register/`           | POST        | Register a new user        |

## Building an APK

The site ships as a PWA (manifest + service worker). To package it as an Android APK:

1. Deploy the site to a public HTTPS URL (Render, Fly.io, Railway, etc.).
2. Go to <https://www.pwabuilder.com/> and paste your URL.
3. Click **Package for Stores → Android** and download the signed APK.

Local LAN testing on Android: run `python manage.py runserver 0.0.0.0:8000`, find your PC's IP with `ipconfig`, then visit `http://<your-ip>:8000` from the phone (same Wi-Fi).

## Project layout

```
littlelemon/
├── littlelemon/        # project settings, urls, wsgi
├── restaurant/         # main app: views, models, templates, API
│   ├── api/            # DRF serializers, views, urls
│   ├── static/
│   └── templates/
├── manage.py
├── requirements.txt
└── .env.example
```
