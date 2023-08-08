from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer
from .forms import EventForm, EventCreateMultiForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required



# @login_required(login_url='login')
# def create_event(request):
#     event_form = EventForm()

#     if request.method == 'POST':
#         event_form = EventForm(request.POST)

#         if event_form.is_valid():
#             ef = event_form.save()
#             created_updated(Event, request)
#             return redirect('event-list')
#     context = {
#         'form': event_form,
#     }
#     return render(request, 'events/create.html', context)

class EventCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = EventCreateMultiForm
    template_name = 'events/create_event.html'
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


# Home Route
def home(request):
    return render(request,'home.html')

# User Register
def register(request):
    form=UserCreationForm
    if request.method=='POST':
        regForm=UserCreationForm(request.POST)
        if regForm.is_valid():
            regForm.save()
            messages.success(request,'User has been registered.')
    return render(request,'registration/register.html',{'form':form})