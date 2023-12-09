# social-network

**backend**
- cd social_network_backend
- source env\bin\activate
- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

**frontend**
- cd social_network_frontend
- npm install
- npm run dev

**notes**
* Before migrating the database, ensure that you have created a new database named "social_network." Then, modify the database credentials inside social_network_backend/social_network_backend/settings.py.
```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'social_network',
            'USER': 'pgadmin',
            'PASSWORD': 'secure_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
```
* If the migration fails, and you receive a "no changes detected" message from makemigrations, attempt to execute makemigrations manually:
    - python manage.py makemigrations account
    - python manage.py makemigrations chat
    - python manage.py makemigrations notification
    - python manage.py makemigrations post
