# Веб-сервис для конвертации аудиофайлов

Веб-сервис реализован на Django с использованием REST API и PostgreSQL.
Выполняет функции создания пользователя, для пользователя - конвертация аудиозаписи формата .wav в формат .mp3.
После успешной конвертации пользователю предаставляется ссылка для скачивания аудиофайла.

Системные требования
----------
* Python 3.7+
* Docker
* Works on Linux, Windows, macOS

## Установка

### Установка ffmpeg.
Установите ffmpeg, используя [инструкцию](https://firstvds.ru/technology/ustanovka-ffmpeg)

### Установка Docker.
Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

### Запуск проекта

Склонируйте репозиторий `git clone https://github.com/iharwest/wavtomp3_TW.git` в текущую папку.

### Настройка проекта

Создайте ```.env``` файл в корне репозитория
Заполнить ```.env``` файл с переменными окружения по примеру:

```
      - DEBUG=1
      - DB_NAME=NAME
      - POSTGRES_USER=USER
      - POSTGRES_PASSWORD=PASSWORD
      - DB_HOST=db
      - DB_PORT=5432
      - SECRET_KEY=SECRET_KEY
```

### Сборка образов и запуск контейнеров

В корне репозитория выполните команду:

```
docker-compose up -d --build
```

### Запустите миграции:

```
docker-compose exec web python manage.py migrate
```

### Остановка контейнеров

Для остановки контейнеров выполните команду:

```
docker-compose stop
```

## Примеры запроса через Postman

### Создание пользователя

Отправьте POST запрос на http://localhost:8000/user/ с телом запроса в формате JSON следующего вида:

```
{
  "username": "example"
}
```

В случае прохождения валиадции данных получите ответ с uuid_token и id пользователя и **статус код 201**.

_Пример ответа:_

```
{
  "id": 0,
  "user_token": "string"
}
```

### Загрузка аудиофайла

Отправьте POST запрос на http://localhost:8000/audio/ с телом запроса в формате  multipart/form-data:

```
"user_id"
"user_token"
"audio_file"
```

В случае прохождения валиадции данных получите ответ с _url_ для скачиванию файла и **статус код 201**.

_Пример ответа:_

```
{
  "url": "string"
}
```

### Скачивание аудиофайла

Отправьте GET запрос на http://localhost:8000/record с параметрами:

```
"id"
"user"
```

В случае прохождения валиадции данных начнется загрузка файла.