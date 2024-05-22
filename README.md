#### Dockerized Flask app with jinja templates and postgres db.

###### What is it
An example of flask app with jinja templates, wtform  and postgres db. Can be used as a starter for simple web app/ Some useful things are missed, see in [notes](#Notes) sections.

###### Build
```bash 
docker compose up --build -d
```

###### Notes
1. This is a fragment of old big app, some useful things are missed.
2. Think about migrations, use alembic.
3. There are no auth, think about native flask-login.
4. Are blueprints old-fashioned or still ok? anyway, tune routing.
5. Think about reliability - exception handling at least. 
6. Gunicorn is here, but nginx is still in demand (and don't forget to log x-request-id).
7. There are no tests at all.
8. Think twice about requirements update.


###### TODO
1. add exception handlers.
2. add backoff
3. add tests
4. add blueprints
