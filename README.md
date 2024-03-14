## Установка проекта
#### Копируем .env
```bash
cp ./.env.example ./.env
```

#### Собираем и запускаем контейнеры
```bash
docker compose -f docker-compose.dev.yml up -d
```

## Управление миграциями

#### Установка go-migrate
(необходима версия v4.16.2)
* https://github.com/golang-migrate/migrate/tree/master/cmd/migrate

#### Применение миграций
```bash
make migrate-up
```

## Управление дампами:

#### Создание pg_dump таблиц со словами и переводами
```bash
docker exec -it <CONTAINER_NAME> sh -c 'pg_dump -U <USER_NAME> --column-inserts -a -t words -t word_translations -t word_examples -t word_example_translations <USER_PASSWORD>' > ./backup_words.sql
```

#### Восстановление базовых слов и переводов из дампа

Восстановление дампов занимает до нескольких минут
```bash
docker exec -i <CONTAINER_NAME> /bin/bash -c "PGPASSWORD=<USER_PASSWORD> psql --username <USER_NAME> <DATABASE_NAME>" < db/backup_words.sql
```
