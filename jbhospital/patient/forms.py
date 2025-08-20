from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "relation", "gender", "dob", "img"]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Enter first name"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Enter last name"
            }),
            "relation": forms.Select(attrs={"class": "form-select"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "dob": forms.DateInput(attrs={
                "class": "form-control", "type": "date"
            }),
            "img": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

        labels = {
            "dob": "Date of Birth",
            "img": "Profile Image",
        }
