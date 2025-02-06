@echo off

REM Create virtual environment
REM python -m venv venv

REM Activate virtual environment
 call venv2\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install required packages
pip install -r requirements.txt

REM Apply migrations
python manage.py migrate

REM Run the Django development server
python manage.py runserver