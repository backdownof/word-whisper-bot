## Создание DB, пользователя и присвоение прав:
#### Заходим в контейнер и для выполнения команд
docker exec -it <CONTAINER_NAME> psql -U root

#### Создаем базу
CREATE DATABASE <DATABASE_NAME>;
#### Создаем пользователя
CREATE USER <USER_NAME> WITH ENCRYPTED PASSWORD '<USER_PASSWORD>';
#### Даем пользователю права на базу данных
GRANT ALL PRIVILEGES ON DATABASE <DATABASE_NAME> TO <USER_NAME>;
ALTER DATABASE <DATABASE_NAME> OWNER TO <USER_PASSWORD>;

## Управление бэкапом базы данных
#### Восстановление базовых слов и переводов из дампа
docker exec -i <CONTAINER_NAME> /bin/bash -c "PGPASSWORD=<USER_PASSWORD> psql --username <USER_NAME> <DATABASE_NAME>" < db/word_translate_dump.sql
