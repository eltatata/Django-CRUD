from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('tasks/', views.tasks_view, name="tasks"),
    path('tasks_completed/', views.completed_tasks_view, name="tasks_completed"),
    path('tasks/create/', views.create_task_view, name="create_tasks"),
    path('tasks/<int:task_id>/', views.task_detail_view, name="tasks_detail"),
    path('tasks/<int:task_id>/complete', views.complete_task, name="complete_task"),
    path('tasks/<int:task_id>/delete', views.delete_task, name="delete_task"),
]
