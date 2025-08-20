from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Appointment
from .forms import AppointmentForm
from mainapp.models import Doctor  # adjust import if different
from django.contrib.auth.mixins import LoginRequiredMixin


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointment_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.doctor = get_object_or_404(Doctor, id=self.kwargs["doctor_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.doctor = self.doctor
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["doctor"] = self.doctor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor"] = self.doctor
        return context

    def get_success_url(self):
        return reverse_lazy("appointments")  # redirect to appointments list page



class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "appointment_list.html"
    context_object_name = "appointments"

    def get_queryset(self):
        # Get only appointments for patients belonging to the logged-in user
        return Appointment.objects.filter(
            patient__user=self.request.user
        ).select_related("doctor", "booked_for", "patient")


from django.contrib import messages
from .models import AppointmentSlots
from .forms import AppointmentSlotsForm

class AppointmentSlotsCreateView(CreateView):
    model = AppointmentSlots
    form_class = AppointmentSlotsForm
    template_name = "add_timeslot.html"
    success_url = reverse_lazy('add_timeslot')  # redirect after successful creation

    def form_valid(self, form):
        messages.success(self.request, "Time slot added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
    


from django.views.generic import TemplateView
from .models import AppointmentSlots, Appointment
from django.utils import timezone
from datetime import timedelta, datetime

class AppointmentCalendarView(TemplateView):
    template_name = "calendar_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all slots grouped by doctor
        doctors = AppointmentSlots.objects.values_list('doctor', flat=True).distinct()
        calendar = []

        # For simplicity, show 7 days from today
        start_date = timezone.localdate()
        dates = [start_date + timedelta(days=i) for i in range(7)]

        # Build calendar structure
        for doctor in doctors:
            slots = AppointmentSlots.objects.filter(doctor_id=doctor)
            doctor_slots = []
            for date in dates:
                day_slots = []
                for slot in slots:
                    # Check if slot is booked
                    appointment = Appointment.objects.filter(
                        booked_for=slot, booking_date=date
                    ).first()
                    day_slots.append({
                        "slot": slot,
                        "appointment": appointment
                    })
                doctor_slots.append({
                    "date": date,
                    "slots": day_slots
                })
            calendar.append({
                "doctor": slots.first().doctor if slots.exists() else None,
                "days": doctor_slots
            })

        context['calendar'] = calendar
        context['dates'] = dates
        return context
