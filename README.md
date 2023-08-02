# package installation 
pip install pipenv
pipenv shell
pipenv install django

# create admin user
python manage.py createsuperuser

# start server
python manage.py runserver

# open test app
http://localhost:8000

# admin portal
http://localhost:8000/admin
