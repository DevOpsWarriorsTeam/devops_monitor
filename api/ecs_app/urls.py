from django.urls import path
from .views import list_clusters, list_services, list_tasks_for_service, user_logout, user_login, list_tasks, container_logs, list_containers, view_logs, restart_service
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('list_clusters/', list_clusters, name='list_clusters'),
    path('list_services/<str:cluster_name>/', list_services, name='list_services'),
    path('list_tasks/<str:cluster_name>/<str:task_arn>/', list_tasks, name='list_tasks'),
    path('list_tasks_for_service/<str:cluster_name>/<str:service_name>/', list_tasks_for_service, name='list_tasks_for_service'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('container/<int:container_id>/logs/', container_logs, name='container-logs'),
    path('list_containers/', list_containers, name='list_containers'),
    path('view_logs/<str:container_name>/', view_logs, name='view_logs'),
    path('restart_service/<str:cluster_name>/<str:service_name>/', restart_service, name='restart-service'),

]