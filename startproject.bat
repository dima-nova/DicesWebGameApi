@echo off

echo Activating virtual environment...
call .\.venv\Scripts\activate

echo Running migrations...
python manage.py makemigrations
python manage.py migrate

echo Starting Django server...
python manage.py runserver

echo All commands executed. Project is running.
pause