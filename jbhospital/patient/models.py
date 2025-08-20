from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class Patient(models.Model):
    RELATION_CHOICES = [
        ('self', 'Self'),
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('spouse', 'Spouse'),
        ('son', 'Son'),
        ('daughter', 'Daughter'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('grandfather', 'Grandfather'),
        ('grandmother', 'Grandmother'),
        ('other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    img = models.ImageField(upload_to='patients/', null=True)
    dob = models.DateField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_relation_display()})"
    
    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

