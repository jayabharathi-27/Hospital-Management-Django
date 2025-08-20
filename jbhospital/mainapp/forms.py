# mainapp/forms.py
from django import forms
from .models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'experience', 'specialization', 'bio', 'profile_image']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years of experience'
            }),
            'specialization': forms.SelectMultiple(attrs={
                'class': 'form-select'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write a short biography'
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

        labels = {
            'name': 'Full Name',
            'experience': 'Experience (years)',
            'specialization': 'Specializations',
            'bio': 'Biography',
            'profile_image': 'Profile Picture',
        }
