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
