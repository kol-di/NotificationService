**Запуск проекта**
1) Склонируйте код проекта в вашу папку
```
git clone https://gitlab.com/kol-di/notificationservice.git
```
2) Создайте и активирйте вирутальное окружение 
```
python -m venv venv
source venv/bin/activate
```
3) Установите зависимости
```
pip install -r requirements.txt
```
4) Для работы с внешним API запустите Redis и Celery
```
redis-server
celery -A Mailing.celery worker --loglevel=info
```
5) Для прогона тестов выполните команду (Опиционально)

```
python manage.py test
```
6) Для запуска сервера выполните
```
python manage.py runserver
```

Сервис доступен оп адресу http://localhost:8000/

Swagger-документация доступна по адресу http://localhost:8000/docs/

Логи сохраняются в корневой папке проекта в файле info.log 

**Дополнительные задания**
1. Организовать тестирование написанного кода.
2. Сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API.
3. Обеспечить подробное логирование на всех этапах обработки запросов.