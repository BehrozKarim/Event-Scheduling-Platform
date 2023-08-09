from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets
from .models import *
from .serializers import EventSerializer
from .forms import EventForm, EventCreateMultiForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class EventCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = EventCreateMultiForm
    template_name = 'create_event.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        evt = form['event'].save()

        return super().form_valid(form)
    
class EventListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Event
    template_name = 'home.html'
    context_object_name = 'events'


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Event
    fields = ['type', 'title', 'organizer', 'description', 'date', 'time', 'location']
    template_name = 'edit_event.html'

class EventDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Event
    template_name = 'delete_event.html'
    success_url = reverse_lazy('event-list')

# User Register
def register(request):
    form=UserCreationForm
    if request.method=='POST':
        regForm=UserCreationForm(request.POST)
        if regForm.is_valid():
            regForm.save()
            messages.success(request,'User has been registered.')
    return render(request,'registration/register.html',{'form':form})

def search_feature(request):
    # Check if the request is a post request.
    print("search_feature", request.method)
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        # Filter your model by the search query
        events = Event.objects.filter(title__contains=search_query)
        return render(request, 'event_search.html', {'query':search_query, 'events':events})
    else:
        return render(request, 'home.html',{})

def attend_event(request, pk):
    print("attend_event", pk)
    queryset = Attendee(user=request.user, event=Event.objects.get(pk=pk))
    queryset.save()
    print("After Save")
    return redirect('event-list')

def attendee_list(request, pk):
    attendees = Attendee.objects.filter(event=pk)
    return render(request, 'attendee_list.html', {'attendees':attendees})

def unattend_event(request, pk):
    attendees = Attendee.objects.filter(event=pk)
    for attendee in attendees:
        if attendee.user == request.user:
            attendee.delete()
            return redirect('event-list')
    return redirect('event-list')