# Bank test task

Run everything
```commandline
docker-compose up
```

Run tests

```commandline
docker-compose run app pytest
```

See docker image commands in `entrypoint.sh`


Make migrations

```commandline
docker-compose run app alembic revision --autogenerate -m "01_initial_migration"
```

Apply migrations

```commandline
docker-compose run app alembic upgrade head
```
