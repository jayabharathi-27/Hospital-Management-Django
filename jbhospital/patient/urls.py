from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_family, name='view_family'),
    path('add/', views.AddMember.as_view(), name='add_member'),
    path('edit/<int:pk>/', views.EditMemberView.as_view(), name='edit_member'),
    path('remove/<int:pk>/', views.RemoveMemberView.as_view(), name='remove_member'),
]
