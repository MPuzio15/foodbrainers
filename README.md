# foodbrainers

It has been written during the Python and Django course in the Codebrainers programming school. 
It is an application that enables the user to sign in and looks for the nearest restaurants based on the user's location. 
Data are stored in the SQL data base. 

In order to see the project visit the following page: https://piscine-maison-07591.herokuapp.com

# Technologies

 - Django
 - SQLite

# In order to open the project, follow the below steps: 
 Install the virtual environment: 
 - pip3 install virtualenv
 - virtualenv -p python3 env
 - source env/bin/activate
 
 Install and start django project: 
 - pip install django
 - django-admin startproject <name>
 - python manage.py startapp polls
 - python manage.py runserver
  
  After that make the required migrations: 
  - python manage.py makemigrations <name>
  - python manage.py migrate

