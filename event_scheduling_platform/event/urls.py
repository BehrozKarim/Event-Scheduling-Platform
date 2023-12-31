from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/',views.register,name='register'),
    path('', views.EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event-edit'),
    path('delete/<int:pk>', views.EventDeleteView.as_view(), name='event-delete'),
    path('event-create/', views.EventCreateView.as_view(), name='event-create'),
    path('search/', views.search_feature, name='search-view'),
    path('attend/<int:pk>', views.attend_event, name='attend-event'),
    path('unattend/<int:pk>', views.unattend_event, name='unattend-event'),
    path('attendees/<int:pk>', views.attendee_list, name='attendees-list'),
]
