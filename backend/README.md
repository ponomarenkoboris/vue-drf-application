# Backend
## Django + Django REST Framework + Channels

### Channel layer uses Redis as its backing store
```shell
docker run -p 6379:6379 -d redis:5
```
### Сreating new migrations
```shell
python manage.py makemigrations
```

### Creating data base
```shell
python manage.py migrate
```

### Start server in development mode
```shell
docker start [Redis backing store container] && python manage.py runserver
```