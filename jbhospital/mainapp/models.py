from django.db import models

class Specialization(models.Model):
    CATEGORY_CHOICES = [
        ('primary_care', 'Primary Care'),
        ('surgical', 'Surgical Specialties'),
        ('medical', 'Medical Specialties (Non-Surgical)'),
        ('womens_health', "Women's & Reproductive Health"),
        ('emergency_critical', 'Emergency & Critical Care'),
        ('diagnostic', 'Diagnostic & Technical Specialties'),
        ('other', 'Other / Specialized Fields'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True)

    def __str__(self):
        return self.title

# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=200) 
    specialization = models.ManyToManyField(Specialization, null=True, related_name='specializations')
    experience = models.PositiveIntegerField()  
    bio = models.TextField(max_length=500, null=True) 
    profile_image = models.ImageField(upload_to='doctors/', null=True)

    def __str__(self):
        return f"Doctor : {self.name}."
