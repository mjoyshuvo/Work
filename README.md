# Youtube API scrapping with Django
Basic Django Project to scrap Youtube api and save video statistics.
## Prerequisites
* Python
* PostgreSql[Important because I've used PostgreSql specific field in django]
* Virtualenv

## Getting Started
1. Clone the repository.
2. Create virtual environment. 
```
virtualenv -p python3 envname --no-site-packages
```
3. Go to project folder.
4. Put ENV variables:
```
create an .env file in root directory of your project. then copy .env.example and put your database related variables in .env file.
```
5. Install requirements 
```
pip install -r requirements.txt
```
6. Migrate 
```
python manage.py migrate
```

7. Import Channel data
```
python manage.py loaddata import_sql/channels.json
```
8. Run project 
```
python manage.py runserver
```
9. Run Scrapping Script[For now I've made a script to run in Crontab command. Later i'll use celery]
```
cd <path_to_your_project>  && <path_to_your_virtualenv_python> manage.py  youtube_scrap
```
## Built With

* [Django](https://www.djangoproject.com/) - The web framework used.
* [Django Rest Framework](http://www.django-rest-framework.org/) - Rest Api.
