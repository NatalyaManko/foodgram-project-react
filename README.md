# praktikum_new_diplom
###### kittygram_final


## О проекте
#### Яндекс Практикум
#### Модуль: Управление проектом на удалённом сервере
### Финальный проект "Контейнеры и CI/CD для Kittygram"

#### Выполненная работа
Настроен автоматическиий запуск тестирования и деплоя проекта Kittygram

![alt text](https://kittygram-frontend-8.prakticum-team.ru/static/media/logo.018b6643f3dd14ed8a10432df1ab2a2b.svg)
### "Better than cats are only kitties" - "Лучше кошек только котята"

#### Описание проекта
Kittygram дает возможность зарегистрированным пользователям посмотреть на других котиков и поделиться изображением своих любимых котиков, добавить новое достижение котика или выбрать достижение из существующих. Можно редактировать или удалить созданного котика.

Проект доступен по доменному имени https://kittygramm.myvnc.com/.

#### Предварительные требования 

###### Системные требования:
- Ubuntu Linux 20.04+;
- или macOS Monterey+;
- или Windows 8+, с WSL2 или HyperV.

- Установленный Docker;
- Установленная утилита Docker Compose.

#### Установка
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/natalyamanko/kittygram_final.git
cd kittigram_final
```
Создать виртуальное окружение
```
python -m venv env
```
Активировать его
```
. env/Scripts/activate
```
Обновить PIP
```
python -m pip install --upgrade pip
```

* Если у вас Linux/macOS
```
     python3 -m venv env

     source env/bin/activate

     python3 -m pip install --upgrade pip
```
Установить зависимости
```
pip install -r requirements.txt
```
Применить миграции
```
python manage.py migrate
```
* Если у вас Linux/macOS
```
     python3 manage.py migrate
```
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
cryptography==42.0.2
defusedxml==0.8.0rc2
Django==3.2.3
django-templated-mail==1.1.1
djangorestframework==3.12.4
djangorestframework-simplejwt==4.8.0
djoser==2.1.0
flake8==6.0.0
flake8-isort==6.0.0
idna==3.6
iniconfig==2.0.0
isort==5.13.2
itypes==1.2.0
Jinja2==3.1.3
MarkupSafe==2.1.5
mccabe==0.7.0
oauthlib==3.2.2
packaging==23.2
Pillow==9.0.0
pluggy==0.13.1
psycopg2-binary==2.9.3
py==1.11.0
pycodestyle==2.10.0
pycparser==2.21
pyflakes==3.0.1
PyJWT==2.8.0
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
python-dotenv==1.0.1
python3-openid==3.2.0
pytz==2024.1
PyYAML==6.0
requests==2.31.0
requests-oauthlib==1.3.1
six==1.16.0
social-auth-app-django==4.0.0
social-auth-core==4.5.2
sqlparse==0.4.4
toml==0.10.2
typing_extensions==4.9.0
uritemplate==4.1.1
urllib3==2.2.0
webcolors==1.11.1
```
**_Контактная информация:_**
Наталья Манько
eMail: manko.nat@mail.ru, natalamanko955@gmail.com
Телефон: +7 913 900 23 23