from django.urls import path
from .views import AppointmentCreateView, AppointmentSlotsCreateView, AppointmentCalendarView, AppointmentListView

urlpatterns = [
     path('', AppointmentListView.as_view(), name='appointments'),
    path("book/<int:doctor_id>/", AppointmentCreateView.as_view(), name="book_appointment"),
    path('add-timeslot/', AppointmentSlotsCreateView.as_view(), name='add_timeslot'),
    path('calendar/', AppointmentCalendarView.as_view(), name='appointment_calendar'),
   
]
