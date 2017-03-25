Django Geocoder
====

Setup
----

```bash
source ./virtualenvs/bin/djangodev/activate

pip install -r requirements.txt
./manage.py migrate
```

Create superuser
----

```bash
./manage.py createsuperuser
```

Run server
----

```bash
./manage.py runserver
```

App will be available at `http://localhost:8000/admin`.

Usage
----

[Video](https://raw.githubusercontent.com/sameoldmadness/django_geocoder/master/media/usage_example.mov)

Cron setup
----

Execute geocode command every 15 minutes.

```
# m h  dom mon dow   command
*/15 * * * * python <path-to-geocoder>/manage.py process_requests
```
