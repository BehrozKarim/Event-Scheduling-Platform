from django.db import models
from django.contrib.auth.models import User
from rest_framework import reverse

class Event(models.Model):
    EVENT_TYPES = [
        ('conference', 'Conference'),
        ('webinar', 'Webinar'),
        ('meetup', 'Meetup'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=EVENT_TYPES, default='conference')

    def __str__(self):
        '''
        This function is used to return the title of the event.
        '''
        return self.title
    
    def get_absolute_url(self):
        '''
        This function is used to return the url of the list of events.
        '''
        return reverse.reverse('event-list')
    


class Attendee(models.Model):
    '''
    This class is used to create an attendee.
    '''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username