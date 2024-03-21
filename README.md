#### foodgram-project-react

## О проекте
#### Яндекс Практикум
### Дипломный проект "Foodgram"

#### Описание проекта
Foodgram предоставляет возможность пользователям публиковать рецепты, добавлять их в избранное, подписываться на авторов и создавать список покупок.

![alt text](https://avatars.mds.yandex.net/i?id=2b5af00556aba4a0bb06a3ca5885c16e-5236455-images-thumbs&n=13)


Проект доступен по доменному имени https://gurman.myftp.biz/.

#### Предварительные требования 

###### Системные требования:
- Ubuntu Linux 20.04+;
- или macOS Monterey+;
- или Windows 8+, с WSL2 или HyperV.

- Установленный Docker;
- Установленная утилита Docker Compose.

#### Установка
Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/natalyamanko/foodgram-project-react.git
cd foodgram_final

Создать виртуальное окружение

python -m venv env

Активировать его

. env/Scripts/activate

Обновить PIP

python -m pip install --upgrade pip

bash


* Если у вас Linux/macOS

bash

 python3 -m venv env

 source env/bin/activate

 python3 -m pip install --upgrade pip

Установить зависимости

pip install -r requirements.txt

Применить миграции

python manage.py migrate

bash

* Если у вас Linux/macOS

 python3 manage.py migrate

markdown

В корневой директории проекта создать файл .env. Заполнить его своими данными, перечень указан в файле .env.example.


#### Запустить автоматический деплой после обновления кода проекта

* На платформе GitHub Actions в разделе Secrets сохранить переменные с необходимыми значениями:
   - DOCKER_USERNAME
   - DOCKER_PASSWORD
   - SSH_KEY
   - SSH_PASSPHRASE
   - USER
   - HOST
   

* Создать коммит и сделать git push

* Подключить Telegram-бота для получения сообщения об успешном завершении деплоя:
   Добавить переменные в Secrets:
   - TELEGRAM_TO
   - TELEGRAM_TOKEN


#### Использованные технологии:
```
asgiref==3.7.2
atomicwrites==1.4.1
attrs==23.2.0
certifi==2024.2.2
cffi==1.16.0
charset-normalizer==3.3.2
colorama==0.4.6
coreapi==2.3.3
coreschema==0.0.4
cryptography==42.0.5
defusedxml==0.8.0rc2
Django==3.2.3
django-colorfield==0.11.0
django-filter==23.5
django-templated-mail==1.1.1
djangorestframework==3.12.4
djangorestframework-simplejwt==4.8.0
djoser==2.1.0
flake8==7.0.0
flake8-isort==6.1.1
gunicorn==20.1.0
idna==3.6
iniconfig==2.0.0
isort==5.13.2
itypes==1.2.0
Jinja2==3.1.3
MarkupSafe==2.1.5
mccabe==0.7.0
oauthlib==3.2.2
packaging==24.0
Pillow==9.0.0
pluggy==0.13.1
psycopg2-binary==2.9.3
py==1.11.0
pycodestyle==2.11.1
pycparser==2.21
pyflakes==3.2.0
PyJWT==2.8.0
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
python-dotenv==0.20.0
python3-openid==3.2.0
pytz==2024.1
PyYAML==6.0
requests==2.31.0
requests-oauthlib==1.4.0
six==1.16.0
social-auth-app-django==4.0.0
social-auth-core==4.5.3
sqlparse==0.4.4
toml==0.10.2
typing_extensions==4.10.0
uritemplate==4.1.1
urllib3==2.2.1
webcolors==1.11.1
```


**_Контактная информация:_**
Наталья Манько
eMail: manko.nat@mail.ru, natalamanko955@gmail.com
Телефон: +7 913 900 23 23
## Для ревью
* Суперпользователь:

- email: manko.nat@mail.ru
- логин: superuser
- пароль: ZuMaISbest

* Администратор:

- email: safari@yandex.ru
- логин: admin
- пароль: ZUMA1234
