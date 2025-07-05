from django.urls import path
from . import views

urlpatterns = [
    path("",views.start_page),
    path("login_page",views.login_page,name='login_page'),
    path("login",views.login_page),
     path('tasks/', views.task_list, name='task_list'),
      path('mark-done/<int:task_id>/', views.mark_task_done, name='mark_done'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
     path('auth/signup/', views.signup_view, name='signup'),
    path('auth/signin/', views.signin_view, name='signin'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
