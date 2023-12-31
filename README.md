# Event-Scheduling-Platform

## How To Setup On Linux
Make sure you have python3 and Django installed.
Also install virtualenv using `python3 -m pip install --user virtualenv` if you don't have it already.

1. Clone This Project `git clone https://github.com/BehrozKarim/Event-Scheduling-Platform.git`
2. Go to Project Directory `cd Event-Scheduling-Platform/event_scheduling_platform`
3. Create a Virtual Environment `python3 -m venv env`
4. Activate Virtual Environment `source env/bin/activate`
5. Install Requirements Package `pip install -r requirements.txt`
6. Migrate Database `python manage.py migrate`
7. Create Super User `python manage.py createsuperuser`
8. Finally Run The Project `python manage.py runserver`

To run the tests use this command `python3 manage.py test event.tests`

## How to use Event Scheduler
1. Go to `http://127.0.0.1:8000/ ` and login with the superuser credentials you created, or you can register a new user from there
2. After logging in, you will be redirected to the home page where you can see all the events
3. You can create a new event by clicking on the `Create Event` button on the top left corner
4. You can edit or delete an event by clicking on the `Edit` or `Delete` button. These buttons will only be visible to the creator of the event
5. You can decide to attend an event by clicking on the `Attend` button.
6. You can view a list of attendees of an event by clicking on the `Attendees-list` button
7. You want yourself to be removed from the attendees list, you can click on the `unattend` button