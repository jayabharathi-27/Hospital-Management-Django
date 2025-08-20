from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop("doctor", None)
        super().__init__(*args, **kwargs)

        if doctor:
            # Initially show all slots for the doctor
            self.fields["booked_for"].queryset = AppointmentSlots.objects.filter(doctor=doctor)
    class Meta:
        model = Appointment
        fields = ["patient", "booked_for", "booking_date"]  # doctor removed

        widgets = {
            "patient": forms.Select(attrs={"class": "form-select"}),
            "booked_for": forms.Select(attrs={"class": "form-select"}),
            "booking_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

        labels = {
            "booked_for": "Select Time Slot",
            "booking_date": "Date",
        }
        


from .models import AppointmentSlots
from mainapp.models import Doctor

class AppointmentSlotsForm(forms.ModelForm):
    class Meta:
        model = AppointmentSlots
        fields = ['doctor', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")
