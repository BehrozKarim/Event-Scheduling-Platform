from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('accounts/register/',views.register,name='register'),
    path('event-list/', views.EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event-edit'),
    path('delete/<int:pk>', views.EventDeleteView.as_view(), name='event-delete'),

]
