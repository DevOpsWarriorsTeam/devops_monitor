from django.shortcuts import render
import boto3
from django.http import JsonResponse
from .utils import extract_last_hash
import subprocess
import json
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import DockerContainer
import docker
import datetime

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Login exitoso'})
        else:
            return JsonResponse({'success': False, 'message': 'Credenciales inválidas'})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True, 'message': 'Logout exitoso'})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def list_clusters(request):
    ecs_client = boto3.client('ecs')
    try:
        response = ecs_client.list_clusters()
        cluster_arns = response.get('clusterArns', [])
        cluster_names = [arn.split('/')[1] for arn in cluster_arns]
        return JsonResponse({'clusters': cluster_names})
    except Exception as e:
        return JsonResponse({'error': str(e)})

def list_services(request, cluster_name):
    ecs_client = boto3.client('ecs')
    response = ecs_client.list_services(cluster=cluster_name)
    service_arns = response.get('serviceArns', [])
    service_info = []
    for service_arn in service_arns:
        service_response = ecs_client.describe_services(cluster=cluster_name, services=[service_arn])
        tasks_info = []
        try:
            tasks_response = ecs_client.list_tasks(cluster=cluster_name, serviceName=service_response['services'][0]['serviceName'])
            task_arns = tasks_response.get('taskArns', [])
            for task_arn in task_arns:
                task_response = ecs_client.describe_tasks(cluster=cluster_name, tasks=[task_arn])
                task_info = {
                    'task_id': task_arn.split('/')[-1],
                    'last_status': task_response['tasks'][0]['lastStatus'],
                    'started_at': task_response['tasks'][0]['createdAt'],
                }
                tasks_info.append(task_info)
        except Exception as e:
            tasks_info.append({'error': str(e)})
        service_info.append({
            'service_arn': service_arn,
            'service_name': service_response['services'][0]['serviceName'],
            'tasks': tasks_info,
        })
    return JsonResponse({'services': service_info})

def list_tasks(request, cluster_name, task_arn):
    ecs_client = boto3.client('ecs')
    try:
        task_response = ecs_client.describe_tasks(cluster=cluster_name, tasks=[task_arn])
        task_info = {
            'task_arn': task_response['tasks'][0]['taskArn'],
            'last_status': task_response['tasks'][0]['lastStatus'],
            'started_at': task_response['tasks'][0]['createdAt'],
        }
        return JsonResponse({'task': task_info})
    except Exception as e:
        return JsonResponse({'error': str(e)})

def list_tasks_for_service(request, cluster_name, service_name):
    try:
        task_arns = subprocess.check_output(['aws', 'ecs', 'list-tasks', '--cluster', cluster_name, '--service', service_name])
        task_arns = json.loads(task_arns)['taskArns']
        tasks_info = []
        for task_arn in task_arns:
            task_hash = extract_last_hash(task_arn)
            task_info = get_task_info_using_describe_tasks(cluster_name, task_hash)
            tasks_info.append(task_info)
        return JsonResponse({'tasks': tasks_info})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def get_task_info_using_describe_tasks(cluster_name, task_id):
    try:
        task_info_json = subprocess.check_output(['aws', 'ecs', 'describe-tasks', '--cluster', cluster_name, '--tasks', task_id])
        task_info = json.loads(task_info_json)['tasks'][0]

        started_at_unix = float(task_info['createdAt'])
        started_at_legible = datetime.datetime.utcfromtimestamp(started_at_unix).strftime('%Y-%m-%d %H:%M:%S')

        formatted_info = {
            'last_status': task_info['lastStatus'],
            'started_at': started_at_legible,
            'task_id': task_id,
        }
        return formatted_info
    except Exception as e:
        return {'error': str(e)}


def restart_service(request, cluster_name, service_name):
    ecs_client = boto3.client('ecs')

    try:
        # Obtener la lista de tareas del servicio
        task_arns = subprocess.check_output(['aws', 'ecs', 'list-tasks', '--cluster', cluster_name, '--service', service_name])
        task_arns = json.loads(task_arns)['taskArns']

        # Detener las tareas del servicio
        for task_arn in task_arns:
            ecs_client.stop_task(cluster=cluster_name, task=task_arn)

        # Actualizar el servicio para reiniciar las tareas
        ecs_client.update_service(cluster=cluster_name, service=service_name)

        response_data = {'success': True, 'message': 'El servicio se reinició correctamente'}
        return JsonResponse(response_data)
    except Exception as e:
        response_data = {'success': False, 'error': str(e)}
        return JsonResponse(response_data)

###VISTAS DE DOCKER LOGS####



def container_logs(request, container_id):
    container = get_object_or_404(DockerContainer, pk=container_id)
    logs = obtener_logs(container_id)
    response_data = {'container_name': container.name, 'logs': logs}
    return JsonResponse(response_data)

def list_containers(request):
    client = docker.from_env()
    containers = client.containers.list()
    containers_data = [
        {'id': container.id, 'name': container.name} for container in containers
    ]
    return JsonResponse({'containers': containers_data})

def view_logs(request, container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    logs = container.logs().decode('utf-8')
    return JsonResponse({'logs': logs})
