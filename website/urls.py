from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('record/<pk>', views.person_record, name='person_record'),
    path('delete/<pk>', views.delete, name='delete'),
    path('add_record', views.add_record, name='add_record'),
    path('edit_record/<pk>', views.edit_record, name='edit_record'),
]
