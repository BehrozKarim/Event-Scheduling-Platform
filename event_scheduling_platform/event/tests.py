from django.test import TestCase
from .forms import NewUserForm
from .models import Event, Attendee
from django.urls import reverse


class EventCreateViewTest(TestCase):
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