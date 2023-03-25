# Тестовое unwinddigital

### Что это

`uparser` - это парсер (одного конкретного xD) Google Sheets [документа](https://docs.google.com/spreadsheets/d/1dYz1KijuuQvToFfdh2-1OpTdVLpfdCQ8z5mnrMZ0VoI/edit#gid=0). 

### Как это работает

**ВАЖНО**: для доступа к API Google используется [service account](https://cloud.google.com/iam/docs/service-account-overview). Данный аккаунт требует наличия разрешений не менее `Browser`, а также доступ на чтение к документу (задаётся в настройках "Share" документа).

Файл с ключом к service account должен помещаться в папке `uparser/credentials`. Полное имя файла следует указать в параметре `SERVICE_ACCOUNT_FILE` внутри `.env`-файла.

Контейнер PostgreSQL разварачивается с некотрыми предустановленными данными (расписание django_q, аккаунт администратора "test_admin:AAA123321")

ETL-процесс запускается по расписанию `Django Q`. По-умолчанию источник в Google Sheets читается каждые 2 минуты.
Настройка расписания доступна в [http://localhost:8000/admin/django_q/](админке django).

### "Серые зоны" ТЗ

- Как обрабытывать противоречивые данные в исходной таблице? 
Текущая реализация принимает за первичный признак пару полей "№ - заказ №". Если в исходных данных присутствует несколько противоречивых данных с одинаковым первичным ключом, в БД будет записано только последнее считанное значение.

- Как обрабатывать неполные или некорректные данные в исходной таблице?
Пытаться сохранить в базу неполную запись? Игнорировать? Останавливать работу?
Текущая реализация не записывает (игнорирует) данные, не прошедшие валидацию на уровне модели и пишет ошибку в лог.

### Как это запустить

1. Скопировать json-файл с ключами от **Google service accout** в папку _uparser/credentials_.
2. Переименовать файл _uparser/.env-sample > .env_, отредактировать при необходимости параметры.
3. Выполнить 
    ```bash
    docker-compose up
    ``` 
    из корневой директории проекта (нужен установленный Docker).