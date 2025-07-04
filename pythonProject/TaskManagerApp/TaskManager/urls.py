from django.urls import path
from . import views

urlpatterns = [
    path("",views.login_page),
    path("task_page",views.task_list),
    path("home",views.login_page),
     path('tasks/', views.task_list, name='task_list'),
      path('mark-done/<int:task_id>/', views.mark_task_done, name='mark_done'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]
