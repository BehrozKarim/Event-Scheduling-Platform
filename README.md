# Event-Scheduling-Platform

## How To Setup On Linux
1. Clone This Project `git clone https://github.com/BehrozKarim/Event-Scheduling-Platform.git`
2. Go to Project Directory `cd Event-Scheduling-Platform/event_scheduling_platform`
3. Create a Virtual Environment `python3 -m venv env`
4. Activate Virtual Environment `source env/bin/activate`
5. Migrate Database `python manage.py migrate`
6. Create Super User `python manage.py createsuperuser`
7. Finally Run The Project `python manage.py runserver`