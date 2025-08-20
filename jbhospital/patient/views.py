from django.shortcuts import render
from .models import Patient
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import PatientForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.
def view_family(request):
    family = Patient.objects.filter(user = request.user)

    context = {
        'people' : family
    }
    template = 'family.html'

    return render(request, template, context)


class AddMember(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'add_patient.html'
    success_url = '/family/'

    def form_valid(self, form):
        # Attach the current user
        form.instance.user = self.request.user

        relation = form.cleaned_data.get("relation")
        gender = form.cleaned_data.get("gender")

        # Uniqueness check for self, mother, father
        if relation in ["self", "mother", "father"]:
            exists = Patient.objects.filter(
                user=self.request.user,
                relation=relation
            )
            if self.object:  # editing case
                exists = exists.exclude(pk=self.object.pk)

            if exists.exists():
                form.add_error("relation", f"You can only have one {relation.title()} in your family.")
                return self.form_invalid(form)

        # Gender rules
        if relation == "mother" and gender != "f":
            form.add_error("gender", "Mother must be Female.")
            return self.form_invalid(form)

        if relation == "father" and gender != "m":
            form.add_error("gender", "Father must be Male.")
            return self.form_invalid(form)

        return super().form_valid(form)
    


class EditMemberView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "edit_member.html"

    def test_func(self):
        # only owner can edit
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Family member updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("view_family")


class RemoveMemberView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Patient
    template_name = "remove_member.html"

    def test_func(self):
        # only owner can delete
        return self.get_object().user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Family member removed successfully.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("view_family")
