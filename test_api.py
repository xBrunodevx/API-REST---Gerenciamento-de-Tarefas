"""
Script de teste simples para a API REST de Gerenciamento de Tarefas
Execute: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_register():
    print("=" * 50)
    print("Testando registro de usuário...")
    url = f"{BASE_URL}/auth/register/"
    data = {
        "username": "testuser",
        "password": "testpass123",
        "password2": "testpass123",
        "email": "test@example.com"
    }
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"Usuário criado: {result.get('user', {}).get('username')}")
        print(f"Tokens recebidos: {'access' in result and 'refresh' in result}")
        return result.get('access')
    else:
        print(f"Erro: {response.text}")
    return None

def test_login():
    print("=" * 50)
    print("Testando login...")
    url = f"{BASE_URL}/auth/login/"
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Tokens recebidos: {'access' in result and 'refresh' in result}")
        return result.get('access')
    else:
        print(f"Erro: {response.text}")
    return None

def test_create_task(token):
    print("=" * 50)
    print("Testando criação de tarefa...")
    url = f"{BASE_URL}/tasks/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Tarefa de teste",
        "description": "Descrição da tarefa de teste",
        "status": "pending"
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"Tarefa criada: {result.get('title')}")
        print(f"ID: {result.get('id')}")
        return result.get('id')
    else:
        print(f"Erro: {response.text}")
    return None

def test_list_tasks(token):
    print("=" * 50)
    print("Testando listagem de tarefas...")
    url = f"{BASE_URL}/tasks/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Total de tarefas: {len(result)}")
        return result
    else:
        print(f"Erro: {response.text}")
    return None

def test_get_task(token, task_id):
    print("=" * 50)
    print(f"Testando obtenção de tarefa {task_id}...")
    url = f"{BASE_URL}/tasks/{task_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Tarefa: {result.get('title')}")
        return result
    else:
        print(f"Erro: {response.text}")
    return None

def test_update_task(token, task_id):
    print("=" * 50)
    print(f"Testando atualização de tarefa {task_id}...")
    url = f"{BASE_URL}/tasks/{task_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Tarefa atualizada",
        "description": "Descrição atualizada",
        "status": "in_progress"
    }
    response = requests.put(url, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Tarefa atualizada: {result.get('title')}")
        print(f"Status: {result.get('status')}")
        return result
    else:
        print(f"Erro: {response.text}")
    return None

def test_delete_task(token, task_id):
    print("=" * 50)
    print(f"Testando exclusão de tarefa {task_id}...")
    url = f"{BASE_URL}/tasks/{task_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 204:
        print("Tarefa excluída com sucesso")
        return True
    else:
        print(f"Erro: {response.text}")
    return False

def main():
    print("Iniciando testes da API REST...")
    print("Certifique-se de que o servidor Django está rodando em http://localhost:8000")
    print()
    
    access_token = test_register()
    if not access_token:
        access_token = test_login()
    
    if access_token:
        task_id = test_create_task(access_token)
        if task_id:
            test_list_tasks(access_token)
            test_get_task(access_token, task_id)
            test_update_task(access_token, task_id)
            test_delete_task(access_token, task_id)
    
    print("=" * 50)
    print("Testes concluídos!")

if __name__ == "__main__":
    main()

