from django.contrib import admin

# Register your models here.
from .models import Specialization, Doctor

admin.site.register(Doctor)
admin.site.register(Specialization)

