## Тестовое задание на должность Python Data Engineer
[ссылка на ТЗ](tz.txt)


## Быстрое описание проекта по ТЗ

>
> - структура БД описана в ./storage/models.py

>- скрипт что бы спарсить данные первых 10 страниц 
./app/search_by_query/fetcher.py

>- sql запросы написаны в ./sql_requests.txt

>- producer и consumer:
./app/search_by_query/producer.py
./app/search_by_query/consumer.py

>- DAG-и в ./dags

*скрипт, консьюмер и продюсер* 

упакованы в docker контейнер **app**, 

запускаются запросами
```console
curl -X 'GET' 'http://localhost:8000/fetcher'
curl -X 'GET' 'http://localhost:8000/consumer'
curl -X 'GET' 'http://localhost:8000/producer'
```

## Как поднять проект?


https
```console
git clone https://github.com/MukhamedZhumabek/test_mp.git && cd test_mp
```
1. Создать сеть для контейнеров
```console
docker network create --driver bridge de-task
```

2. Поднять проект который включает сервисы, которые занимают порты
 - app(fastapi)        :8000
 - db(postgresql) :5433
 - kafka      :9092
 - zookeeper  :2181
```console
docker-compose up -d
```

3. Поднять Airflow, который включает сервисы, которые занимают порты
 - airflow_postgresql 
 - airflow_webserver  :8080
 - airflow_sheduler 
```console
cd airflow_service && docker-compose up -d && cd ..
```
## Логи
- логи уровня warning и выше пишутся в log/error.log
- вcе логи в реальном времени можно посмотреть корневой директории

все логи 
```console
docker-compose logs -f
```

только логи приложения
```console
docker-compose logs app -f
```

## Запустить скрипт "для сбора данных 10 страниц по запросу 'куртка' "

```console
curl -X 'GET' 'http://localhost:8000/fetcher'
```
или 
>запустить fetcher запрос в [openapi](http://127.0.0.1:8000/docs)

посмотреть логи только скрипта

```console
docker-compose logs app -f | grep app.fetcher
```

## Запустить consumer и producer

- логин:admin
- пароль: admin

[зайти на локально поднятый Airflow Webserver](http://127.0.0.1:8080)

посмотреть только логи консьюмера 
```console
docker-compose logs app -f | grep app.consumer
```

посмотреть только логи продюсера 
```console
docker-compose logs app -f | grep app.producer
```

### Подключитья к базе c DataGrip, DBeaver, etc:
```console
 POSTGRES_USER: de_app
 POSTGRES_PASSWORD: de_password
 POSTGRES_DB: de_db
 POSTGRES_HOST: localhost
 POSTGRES_PORT: 5433
```
