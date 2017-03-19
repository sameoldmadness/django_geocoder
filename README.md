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

TODO
----

- catch api errors (and record failed responses)
- set up cron job
- exclude exausted providers
- test yandex and google keys
- squash migrations
- remove gui restrictions
- add columns settings
- smth wrong with oss coords
- save full text string
- RecursionError at /admin/geocoder/address/14/change/
