# Приложение для голосований

## Для начала работы необходимо:

- Установить зависимости в виртуальное окружение из файла requirements.txt 
  >pip install -r requirements.txt
- Создать миграции
  >python manage.py makemigrations
- Применить миграции
  >python manage.py migrate
- Создать суперпользователя
  >python manage.py createsuperuser
- Запустить сервер RabbitMQ
  >rabbitmq-server start
- Запустить Celery worker
  >celery -A some_project worker -l info
- Установить переменные окружения 'EMAIL_HOST_USER' и 'EMAIL_HOST_PASSWORD' для отправки почты с результатами голосований. Также изменить прочие email настройки в settings.py при необходимости

---

## Адреса API:

- /voting/list - Список всех голосований. Может принимать параметр запроса *is_active* Для фильтрации по активности голосования
- /voting/detail/\<pk> - Подробная информация о голосовании (pk - id голосования)
- /voting/participants/\<pk> - Информация об участниках голосования (pk - id голосования)
- /voting/winners - Список всех законченных голосований с их победителями
- /voting/vote/\<pk> - Добавление одного голоса к кандидату (pk - id персонажа на голосовании)

---

## Выгрузка xlsx файла на email

Пользователи, которые имеют доступ к административной панели и имеют привязанную к аккаунту электронную почту, могут отправить себе на почту файл в формате xlsx с результатами выбранного голосования, нажав на кнопку **send** на странице /admin/app_voting/voting/