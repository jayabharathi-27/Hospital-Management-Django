from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import DoctorForm
from .models import Doctor, Specialization
# Create your views here.

class HomeView(ListView):
    model = Doctor
    template_name = 'home.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return Doctor.objects.prefetch_related('specialization')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specializations'] = Specialization.objects.all().order_by('title')
        return context

from django.views.generic import ListView
from .models import Doctor, Specialization

class DoctorsView(ListView):
    model = Doctor
    template_name = 'doctors.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        queryset = Doctor.objects.prefetch_related('specialization')
        
        # Optional: filter by specialization from URL query param ?specialization=Cardiology
        specialization_title = self.request.GET.get('specialization')
        if specialization_title:
            queryset = queryset.filter(specialization__title=specialization_title)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specializations'] = Specialization.objects.all().order_by('title')
        context['selected_specialization'] = self.request.GET.get('specialization', '')
        return context



def aboutView(request):
    template = 'about.html'
    context = {
         
    }
    return render(request, template, context)

def contactView(request):
    template = 'contact.html'
    context = {
         
    }
    return render(request, template, context)


class AddDoctor(CreateView):
    model = Doctor
    template_name = 'add_doctor.html'
    form_class = DoctorForm
    success_url = '/'

class DoctorDetails(DetailView):
    model = Doctor
    template_name = 'doctor_details.html'
    context_object_name = 'doctor'

class EditDoctor(UpdateView):
    model = Doctor
    template_name = 'edit_doctor.html'
    fields = '__all__'
    success_url = '/'

class DeleteDoctor(DeleteView):
    model = Doctor
    template_name = 'del_doctor.html'
    success_url = '/'


def searchView(request):
    query = request.GET.get('q')
    result_doctors = Doctor.objects.filter(title__icontains = query)
    context = {
        'query' : query,
        'doctors' : result_doctors
    }
    template = 'search_results.html'

    return render(request, template, context)