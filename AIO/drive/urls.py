from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('folder/<str:folder_name>/', views.view_folder, name='view_folder'),
    path('upload/', views.upload_file, name='upload_file'),
    path('create_folder/', views.create_folder, name='create_folder'),
    re_path(r'^delete_folder/(?P<folder_name>.+)/$', views.delete_folder, name='delete_folder'),
    path('download/<path:file_name>/', views.download_file, name='download_file'),
    path('delete/<path:file_name>/', views.delete_file, name='delete_file'),
]
