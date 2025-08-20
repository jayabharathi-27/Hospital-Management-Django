from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'homepage'),
    path('about', views.aboutView, name = 'aboutpage'),
    path('contact', views.contactView, name = 'contactpage'),
    path('all', views.DoctorsView.as_view(), name='doctors'),
    path('doctors/add', views.AddDoctor.as_view(), name = 'add_doctor'),
    path('doctor/<int:pk>', views.DoctorDetails.as_view(), name= 'doc_details'),
    path('doctor/status/<int:pk>', views.EditDoctor.as_view(), name = 'edit_doctor'),
    path('doctor/cancel/<int:pk>', views.DeleteDoctor.as_view(), name = 'del_doctor'),
    path('search/', views.searchView, name = 'search_doctors')
]