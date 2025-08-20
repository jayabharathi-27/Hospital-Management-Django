from django.core.exceptions import ValidationError
from django.db import models
from patient.models import Patient
from mainapp.models import Doctor


class AppointmentSlots(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="slots")
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.doctor} | {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("booked", "Booked"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    doctor = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments"
    )
    booked_for = models.ForeignKey(
        AppointmentSlots, on_delete=models.CASCADE, related_name="appointments"
    )
    booking_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="booked")
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "booked_for", "booking_date"],
                name="unique_doctor_slot_per_day",
            ),
            models.UniqueConstraint(
                fields=["patient", "booked_for", "booking_date"],
                name="unique_patient_slot_per_day",
            ),
        ]
        ordering = ["-booking_date", "-booked_at"]

    def clean(self):
        # Doctor double booking check
        if Appointment.objects.filter(
            doctor=self.doctor,
            booked_for=self.booked_for,
            booking_date=self.booking_date,
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                {"booked_for": "This time slot is already booked for this doctor."}
            )

        # Patient double booking check
        if Appointment.objects.filter(
            patient=self.patient,
            booked_for=self.booked_for,
            booking_date=self.booking_date,
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                {"booked_for": "You have already booked this time slot."}
            )

    def __str__(self):
        return f"{self.patient} → {self.doctor} on {self.booking_date} at {self.booked_for.start_time}"
