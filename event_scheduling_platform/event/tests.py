from django.test import TestCase
from .forms import NewUserForm, EventForm, EventCreateMultiForm
from .models import Event, Attendee
from django.urls import reverse


class ViewTests(TestCase):
    def setUp(self):
        user_data = {
            'username': 'test_user',
            'email': 'first@gmail.com',
            'password1': 'First@Second67',
            'password2': 'First@Second67',
        }

        form = NewUserForm(data=user_data)
        self.assertTrue(form.is_valid())
        self.user = form.save()
        self.assertEqual(self.user.username, 'test_user')
        self.client.force_login(self.user)
    
    def test_user_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
    

    def test_event_creation(self):
        form_data = {
            'type': 'Conference',
            'title': 'Test Event',
            'date': '2023-08-15',
            'time': '12:00:00',
            'location': 'Test Location',
            'description': 'Test Description',
        }
        response = self.client.post(reverse('event-create'), data=form_data)
        self.assertEqual(response.status_code, 200)  # Redirect to success_url

    def test_event_creation_invalid_form(self):
        # Create an invalid form (e.g., missing required fields)
        form_data = {}
        response = self.client.post(reverse('event-create'), data=form_data)

        self.assertEqual(response.status_code, 200)
    
    def test_event_creation_template(self):
        response = self.client.get(reverse('event-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_event.html')

    def test_event_list(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_event_update(self):
        event = Event.objects.create(
            type='Conference',
            title='Test Event',
            date='2023-08-15',
            time='12:00:00',
            location='Test Location',
            description='Test Description',
            organizer=self.user,
        )
        response = self.client.get(reverse('event-edit', kwargs={'pk': event.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_event_delete(self):
        event = Event.objects.create(
            type='Conference',
            title='Test Event',
            date='2023-08-15',
            time='12:00:00',
            location='Test Location',
            description='Test Description',
            organizer=self.user,
        )
        response = self.client.get(reverse('event-delete', kwargs={'pk': event.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_create_attendee(self):
        event = Event.objects.create(
            type='Conference',
            title='Test Event',
            date='2023-08-15',
            time='12:00:00',
            location='Test Location',
            description='Test Description',
            organizer=self.user,
        )
        response = self.client.get(reverse('attend-event', kwargs={'pk': event.pk}))
        self.assertEqual(response.status_code, 302)

    def test_attendee_list(self):
        event = Event.objects.create(
            type='Conference',
            title='Test Event',
            date='2023-08-15',
            time='12:00:00',
            location='Test Location',
            description='Test Description',
            organizer=self.user,
        )
        Attendee.objects.create(
            user=self.user,
            event=event,
        )      
        response = self.client.get(reverse('attendees-list', kwargs={'pk': event.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_attendee_delete(self):
        event = Event.objects.create(
            type='Conference',
            title='Test Event',
            date='2023-08-15',
            time='12:00:00',
            location='Test Location',
            description='Test Description',
            organizer=self.user,
        )
        
        Attendee.objects.create(
            user=self.user,
            event=event,
        )

        response = self.client.get(reverse('unattend-event', kwargs={'pk': event.pk}))
        self.assertEqual(response.status_code, 302)

class ModelTests(TestCase):
    def setUp(self):
        user_data = {
            'username': 'test_user',
            'email': 'first@gmail.com',
            'password1': 'First@Second67',
            'password2': 'First@Second67',
        }

        form = NewUserForm(data=user_data)
        self.assertTrue(form.is_valid())
        self.user = form.save()
        self.assertEqual(self.user.username, 'test_user')
        self.client.force_login(self.user)

    def test_event_model(self):
        event = Event.objects.create(
            type='Conference',
            title='Test Event',
            date='2023-08-15',
            time='12:00:00',
            location='Test Location',
            description='Test Description',
            organizer=self.user,
        )
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.type, 'Conference')
        self.assertEqual(event.organizer, self.user)
        self.assertEqual(event.description, 'Test Description')
        self.assertEqual(event.date, '2023-08-15')
        self.assertEqual(event.time, '12:00:00')
        self.assertEqual(event.location, 'Test Location')
    
    def test_attendee_model(self):
        event = Event.objects.create(
            type='Conference',
            title='Test Event',
            date='2023-08-15',
            time='12:00:00',
            location='Test Location',
            description='Test Description',
            organizer=self.user,
        )
        attendee = Attendee.objects.create(
            user=self.user,
            event=event,
        )
        self.assertEqual(attendee.user, self.user)
        self.assertEqual(attendee.event, event)

class FormTests(TestCase):
    def setUp(self):
        user_data = {
            'username': 'test_user',
            'email': 'first@gmail.com',
            'password1': 'First@Second67',
            'password2': 'First@Second67',
        }

        form = NewUserForm(data=user_data)
        self.assertTrue(form.is_valid())
        self.user = form.save()
        self.assertEqual(self.user.username, 'test_user')
        self.client.force_login(self.user)
    
    def test_event_form(self):
        form_data = {
            'type': 'conference',
            'title': 'Test Event',
            'description': 'Test Description',
            'date': '2023-08-15',
            'time': '12:00:00',
            'location': 'Test Location',
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())
        event = form.save(commit=False)
        event.organizer = self.user
        event.save()
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.type, 'conference')
        self.assertEqual(event.organizer, self.user)
        self.assertEqual(event.description, 'Test Description')
        self.assertEqual(event.location, 'Test Location')
    
    def test_event_form_invalid(self):
        form_data = {
            'type': 'conference',
            'title': 'Test Event',
            'description': 'Test Description',
            'date': '2023-08-15',
            'time': '12:00:00',
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        form_data = {
            'event-type': 'conference',
            'event-title': 'Test Event',
            'event-description': 'Test Description',
            'event-date': '2023-08-15',
            'event-time': '12:00:00',
            'event-location': 'Test Location',
        }
        form = EventCreateMultiForm(data=form_data)
        self.assertTrue(form.is_valid())
        event = form['event'].save(commit=False)
        event.organizer = self.user
        event.save()
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.type, 'conference')
        self.assertEqual(event.organizer, self.user)
        self.assertEqual(event.description, 'Test Description')
        self.assertEqual(event.location, 'Test Location')
        