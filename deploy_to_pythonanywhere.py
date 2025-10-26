#!/usr/bin/env python3
"""
Script automatizado para desplegar Burritos To Go en PythonAnywhere
Autor: GitHub Copilot CLI
Fecha: 2025-01-26
"""

import requests
import json
import time
import sys
from pathlib import Path

# Configuración
USERNAME = 'pradodiazbackend'
TOKEN = '4b299407e0f84fd583a1aa029676fe51884b1b48'
DOMAIN = f'{USERNAME}.pythonanywhere.com'
REPO_URL = 'https://github.com/BernardoPD/burritos-to-go-api.git'
PROJECT_NAME = 'burritos-to-go-api'
PYTHON_VERSION = '3.10'

# Headers para la API
headers = {'Authorization': f'Token {TOKEN}'}
base_url = 'https://www.pythonanywhere.com/api/v0'

def print_step(step_num, message):
    """Imprime un paso del proceso"""
    print(f"\n{'='*60}")
    print(f"📍 PASO {step_num}: {message}")
    print(f"{'='*60}")

def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime mensaje de error"""
    print(f"❌ {message}")

def print_info(message):
    """Imprime mensaje informativo"""
    print(f"ℹ️  {message}")

def check_existing_webapp():
    """Verifica si ya existe una web app"""
    print_step(1, "VERIFICANDO WEB APP EXISTENTE")
    
    url = f'{base_url}/user/{USERNAME}/webapps/'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        webapps = response.json()
        if webapps:
            print_info(f"Se encontraron {len(webapps)} web app(s) existente(s)")
            for app in webapps:
                domain = app.get('domain_name', 'N/A')
                print_info(f"  - {domain}")
            
            # Eliminar web app existente si es necesario
            for app in webapps:
                domain = app.get('domain_name')
                if domain == DOMAIN:
                    print_info(f"Eliminando web app existente: {domain}")
                    delete_url = f'{base_url}/user/{USERNAME}/webapps/{domain}/'
                    delete_response = requests.delete(delete_url, headers=headers)
                    if delete_response.status_code == 200:
                        print_success("Web app eliminada correctamente")
                        time.sleep(2)
                    else:
                        print_error(f"Error al eliminar web app: {delete_response.status_code}")
        else:
            print_info("No hay web apps existentes")
        return True
    else:
        print_error(f"Error al verificar web apps: {response.status_code}")
        return False

def create_webapp():
    """Crea una nueva web app en PythonAnywhere"""
    print_step(2, "CREANDO WEB APP")
    
    url = f'{base_url}/user/{USERNAME}/webapps/'
    
    data = {
        'domain_name': DOMAIN,
        'python_version': f'python{PYTHON_VERSION.replace(".", "")}'  # python310
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print_success(f"Web app creada: {DOMAIN}")
        return True
    elif response.status_code == 409:
        print_info("La web app ya existe, continuando...")
        return True
    else:
        print_error(f"Error al crear web app: {response.status_code}")
        print_error(f"Respuesta: {response.text}")
        return False

def execute_bash_command(command, description):
    """Ejecuta un comando en la consola bash de PythonAnywhere"""
    print_info(f"Ejecutando: {description}")
    
    # Crear consola
    console_url = f'{base_url}/user/{USERNAME}/consoles/'
    console_response = requests.post(
        console_url,
        headers=headers,
        json={'executable': 'bash', 'arguments': []}
    )
    
    if console_response.status_code != 201:
        print_error(f"Error al crear consola: {console_response.status_code}")
        return False
    
    console_id = console_response.json()['id']
    print_info(f"Consola creada: {console_id}")
    
    # Enviar comando
    input_url = f'{base_url}/user/{USERNAME}/consoles/{console_id}/send_input/'
    input_data = {'input': f'{command}\n'}
    
    input_response = requests.post(input_url, headers=headers, json=input_data)
    
    if input_response.status_code == 200:
        time.sleep(2)  # Esperar a que el comando se ejecute
        
        # Obtener salida
        output_url = f'{base_url}/user/{USERNAME}/consoles/{console_id}/get_latest_output/'
        output_response = requests.get(output_url, headers=headers)
        
        if output_response.status_code == 200:
            output = output_response.json().get('output', '')
            if output:
                print(f"   Salida: {output[:200]}...")
        
        # Cerrar consola
        kill_url = f'{base_url}/user/{USERNAME}/consoles/{console_id}/'
        requests.delete(kill_url, headers=headers)
        
        print_success(f"{description} - Completado")
        return True
    else:
        print_error(f"Error al ejecutar comando: {input_response.status_code}")
        return False

def configure_webapp():
    """Configura la web app con WSGI y static files"""
    print_step(3, "CONFIGURANDO WEB APP")
    
    # Configurar source directory
    print_info("Configurando source directory...")
    url = f'{base_url}/user/{USERNAME}/webapps/{DOMAIN}/'
    
    data = {
        'source_directory': f'/home/{USERNAME}/{PROJECT_NAME}'
    }
    
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print_success("Source directory configurado")
    else:
        print_error(f"Error al configurar source directory: {response.status_code}")
    
    # Configurar virtualenv
    print_info("Configurando virtualenv...")
    data = {
        'virtualenv_path': f'/home/{USERNAME}/.virtualenvs/burritos_env'
    }
    
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print_success("Virtualenv configurado")
    else:
        print_error(f"Error al configurar virtualenv: {response.status_code}")
    
    return True

def configure_static_files():
    """Configura los archivos estáticos"""
    print_step(4, "CONFIGURANDO ARCHIVOS ESTÁTICOS")
    
    static_files = [
        {
            'url': '/static/',
            'path': f'/home/{USERNAME}/{PROJECT_NAME}/staticfiles'
        },
        {
            'url': '/media/',
            'path': f'/home/{USERNAME}/{PROJECT_NAME}/media'
        }
    ]
    
    for static in static_files:
        url = f'{base_url}/user/{USERNAME}/webapps/{DOMAIN}/static_files/'
        
        response = requests.post(url, headers=headers, json=static)
        
        if response.status_code == 201:
            print_success(f"Configurado: {static['url']} → {static['path']}")
        elif response.status_code == 409:
            print_info(f"Ya existe: {static['url']}")
        else:
            print_error(f"Error al configurar {static['url']}: {response.status_code}")
    
    return True

def reload_webapp():
    """Recarga la web app"""
    print_step(5, "RECARGANDO WEB APP")
    
    url = f'{base_url}/user/{USERNAME}/webapps/{DOMAIN}/reload/'
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        print_success("Web app recargada correctamente")
        return True
    else:
        print_error(f"Error al recargar web app: {response.status_code}")
        print_error(f"Respuesta: {response.text}")
        return False

def print_instructions():
    """Imprime las instrucciones finales"""
    print("\n" + "="*60)
    print("🎉 DEPLOYMENT INICIADO EN PYTHONANYWHERE")
    print("="*60)
    
    print("\n📋 PRÓXIMOS PASOS MANUALES EN PYTHONANYWHERE:")
    print("\n1. Ve a: https://www.pythonanywhere.com/user/pradodiazbackend/")
    print("   → Click en 'Consoles' → 'Bash'")
    
    print("\n2. Ejecuta estos comandos EN ORDEN:")
    
    print("\n   # Clonar repositorio")
    print(f"   git clone {REPO_URL}")
    print(f"   cd {PROJECT_NAME}")
    
    print("\n   # Crear entorno virtual")
    print(f"   mkvirtualenv --python=/usr/bin/python{PYTHON_VERSION} burritos_env")
    
    print("\n   # Instalar dependencias")
    print("   pip install -r requirements.txt")
    
    print("\n   # Configurar settings.py")
    print("   nano burritos_project/settings.py")
    print("   # Cambiar:")
    print("   #   DEBUG = False")
    print(f"   #   ALLOWED_HOSTS = ['{DOMAIN}']")
    print("   #   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')")
    
    print("\n   # Migrar base de datos")
    print("   python manage.py migrate")
    
    print("\n   # Recolectar archivos estáticos")
    print("   python manage.py collectstatic --noinput")
    
    print("\n3. Configurar WSGI file:")
    print(f"   Ve a: Web → {DOMAIN} → WSGI configuration file")
    print("   Reemplaza todo el contenido con:")
    
    print(f"""
   import os
   import sys
   
   path = '/home/{USERNAME}/{PROJECT_NAME}'
   if path not in sys.path:
       sys.path.append(path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   """)
    
    print("\n4. Subir base de datos:")
    print("   → Files → Upload a file")
    print(f"   → Navega a: /home/{USERNAME}/{PROJECT_NAME}/")
    print("   → Sube tu archivo: db.sqlite3")
    
    print("\n5. Reload web app:")
    print(f"   → Web → {DOMAIN} → Reload")
    
    print("\n" + "="*60)
    print("🌐 URLs DE TU APLICACIÓN:")
    print("="*60)
    print(f"\n  API REST:        https://{DOMAIN}/api/")
    print(f"  Dashboard Cliente: https://{DOMAIN}/api/panel/")
    print(f"  Dashboard Admin:   https://{DOMAIN}/api/admin-panel/")
    print(f"  Django Admin:      https://{DOMAIN}/admin/")
    
    print("\n" + "="*60)
    print("📚 DOCUMENTACIÓN COMPLETA:")
    print("="*60)
    print("\n  Ver: DEPLOYMENT_PYTHONANYWHERE.md")
    print("  Para guía detallada paso a paso")
    
    print("\n✅ El deployment está configurado parcialmente.")
    print("⚠️  Completa los pasos manuales arriba para finalizar.\n")

def main():
    """Función principal"""
    print("\n" + "="*60)
    print("🚀 BURRITOS TO GO - DEPLOYMENT AUTOMÁTICO")
    print("="*60)
    print(f"\nUsuario: {USERNAME}")
    print(f"Dominio: {DOMAIN}")
    print(f"Repositorio: {REPO_URL}")
    
    try:
        # Paso 1: Verificar y limpiar web apps existentes
        if not check_existing_webapp():
            sys.exit(1)
        
        # Paso 2: Crear web app
        if not create_webapp():
            sys.exit(1)
        
        # Paso 3: Configurar web app
        if not configure_webapp():
            sys.exit(1)
        
        # Paso 4: Configurar static files
        if not configure_static_files():
            sys.exit(1)
        
        # Mostrar instrucciones finales
        print_instructions()
        
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
