from django.urls import path
from . import views

app_name = 'student_progress'

urlpatterns = [
    path('', views.index, name='index'),
    path('views/', views.view_xml_files, name='views'),
    path('add_xml', views.add_xml_file, name='add_xml'),
    path('view_file/<str:filename>/', views.view_single_xml, name='view_single_xml'),
    path('save_xml/<str:filename>/', views.save_xml, name='save_xml'),
    path('database/', views.view_db, name='view_db'),
    path('update_all/', views.update_all, name='update_all'),
    path('delete/<int:id>/', views.delete_grade, name='delete_grade')
]