"""
Script automatizado para desplegar Burritos To Go en PythonAnywhere
Autor: Sistema de Deployment Automatizado
Fecha: 2025-10-26
"""

import requests
import json
import time

# Credenciales de PythonAnywhere
USERNAME = 'pradodiazbackend'
API_TOKEN = '4b299407e0f84fd583a1aa029676fe51884b1b48'
PASSWORD = 'Fw$*R(STC3eM7M3'
BASE_URL = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}'
HEADERS = {'Authorization': f'Token {API_TOKEN}'}

# Configuración del proyecto
REPO_URL = 'https://github.com/BernardoPD/burritos-to-go-api.git'
DOMAIN = f'{USERNAME}.pythonanywhere.com'

def print_status(message, status='INFO'):
    """Imprime mensajes con formato"""
    symbols = {'INFO': '📋', 'SUCCESS': '✅', 'ERROR': '❌', 'WARNING': '⚠️'}
    print(f"\n{symbols.get(status, '•')} {message}")

def make_request(method, url, **kwargs):
    """Realiza una petición HTTP con manejo de errores"""
    try:
        response = requests.request(method, url, headers=HEADERS, **kwargs)
        return response
    except Exception as e:
        print_status(f"Error en request: {str(e)}", 'ERROR')
        return None

def execute_console_command(command, description=""):
    """Ejecuta un comando en la consola de PythonAnywhere"""
    print_status(f"Ejecutando: {description or command}", 'INFO')
    
    # Crear consola
    console_url = f'{BASE_URL}/consoles/'
    response = make_request('POST', console_url, json={'executable': 'bash'})
    
    if not response or response.status_code != 200:
        print_status(f"Error creando consola: {response.text if response else 'No response'}", 'ERROR')
        return False
    
    console_id = response.json()['id']
    time.sleep(2)
    
    # Enviar comando
    input_url = f'{BASE_URL}/consoles/{console_id}/send_input/'
    response = make_request('POST', input_url, json={'input': f'{command}\n'})
    
    time.sleep(3)
    
    # Obtener output
    output_url = f'{BASE_URL}/consoles/{console_id}/get_latest_output/'
    response = make_request('GET', output_url)
    
    if response and response.status_code == 200:
        output = response.json().get('output', '')
        print(output)
    
    # Cerrar consola
    make_request('DELETE', f'{BASE_URL}/consoles/{console_id}/')
    
    return True

def create_database():
    """Crea la base de datos MySQL en PythonAnywhere"""
    print_status("Creando base de datos MySQL...", 'INFO')
    
    db_url = f'{BASE_URL}/mysql/databases/'
    response = make_request('POST', db_url, json={'name': 'burritos_db'})
    
    if response and response.status_code in [200, 201]:
        print_status("Base de datos creada exitosamente", 'SUCCESS')
        return True
    elif response and 'already exists' in response.text.lower():
        print_status("La base de datos ya existe", 'WARNING')
        return True
    else:
        print_status(f"Error creando BD: {response.text if response else 'No response'}", 'ERROR')
        return False

def setup_webapp():
    """Configura la webapp en PythonAnywhere"""
    print_status("Configurando Web App...", 'INFO')
    
    webapp_url = f'{BASE_URL}/webapps/'
    
    # Verificar si ya existe
    response = make_request('GET', f'{webapp_url}{DOMAIN}/')
    
    if response and response.status_code == 200:
        print_status("Web App ya existe, actualizando...", 'WARNING')
    else:
        # Crear nueva webapp
        response = make_request('POST', webapp_url, json={
            'domain_name': DOMAIN,
            'python_version': 'python311'
        })
        
        if response and response.status_code in [200, 201]:
            print_status("Web App creada exitosamente", 'SUCCESS')
        else:
            print_status(f"Error creando webapp: {response.text if response else 'No response'}", 'ERROR')
            return False
    
    return True

def deploy_project():
    """Despliega el proyecto completo"""
    print_status("=== INICIANDO DEPLOYMENT EN PYTHONANYWHERE ===", 'INFO')
    
    # Paso 1: Crear base de datos
    if not create_database():
        return False
    
    # Paso 2: Configurar webapp
    if not setup_webapp():
        return False
    
    # Paso 3: Clonar repositorio
    print_status("Clonando repositorio desde GitHub...", 'INFO')
    execute_console_command(
        f'cd ~ && rm -rf burritos-to-go-api && git clone {REPO_URL}',
        "Clonando repositorio"
    )
    
    # Paso 4: Crear virtualenv
    print_status("Creando entorno virtual...", 'INFO')
    execute_console_command(
        f'cd ~ && mkvirtualenv --python=/usr/bin/python3.11 burritos_env',
        "Creando virtualenv"
    )
    
    # Paso 5: Instalar dependencias
    print_status("Instalando dependencias...", 'INFO')
    execute_console_command(
        f'workon burritos_env && cd ~/burritos-to-go-api && pip install -r requirements.txt && pip install mysqlclient',
        "Instalando paquetes Python"
    )
    
    # Paso 6: Configurar settings.py para producción
    print_status("Configurando settings para producción...", 'INFO')
    settings_content = f"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-+ye3din#vjy9f3-eu_+rnpaqh6r4g+8!wgax_ulyi8=-d1w+r5"

DEBUG = False

ALLOWED_HOSTS = ['{DOMAIN}', 'www.{DOMAIN}']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework.authtoken',
    'core',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "burritos_project.urls"

TEMPLATES = [
    {{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {{
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        }},
    }},
]

WSGI_APPLICATION = "burritos_project.wsgi.application"

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{USERNAME}$burritos_db',
        'USER': '{USERNAME}',
        'PASSWORD': '{PASSWORD}',
        'HOST': '{USERNAME}.mysql.pythonanywhere-services.com',
        'OPTIONS': {{
            'charset': 'utf8mb4',
        }}
    }}
}}

AUTH_PASSWORD_VALIDATORS = [
    {{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"}},
    {{"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}},
    {{"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"}},
    {{"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"}},
]

AUTH_USER_MODEL = 'core.Usuario'

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/api/panel/'
LOGOUT_REDIRECT_URL = '/admin/login/'
"""
    
    # Guardar settings.py
    execute_console_command(
        f'cat > ~/burritos-to-go-api/burritos_project/settings.py << \'EOFMARKER\'\n{settings_content}\nEOFMARKER',
        "Configurando settings.py"
    )
    
    # Paso 7: Crear archivo WSGI
    print_status("Configurando archivo WSGI...", 'INFO')
    wsgi_content = f"""
import os
import sys

path = '/home/{USERNAME}/burritos-to-go-api'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""
    
    execute_console_command(
        f'cat > /var/www/{USERNAME}_pythonanywhere_com_wsgi.py << \'EOFMARKER\'\n{wsgi_content}\nEOFMARKER',
        "Configurando WSGI"
    )
    
    # Paso 8: Ejecutar migraciones
    print_status("Ejecutando migraciones de base de datos...", 'INFO')
    execute_console_command(
        f'workon burritos_env && cd ~/burritos-to-go-api && python manage.py migrate',
        "Aplicando migraciones"
    )
    
    # Paso 9: Colectar archivos estáticos
    print_status("Colectando archivos estáticos...", 'INFO')
    execute_console_command(
        f'workon burritos_env && cd ~/burritos-to-go-api && python manage.py collectstatic --noinput',
        "Colectando static files"
    )
    
    # Paso 10: Crear superusuario admin
    print_status("Creando superusuario admin...", 'INFO')
    create_admin_script = """
from core.models import Usuario
from django.db import IntegrityError

try:
    if not Usuario.objects.filter(username='admin').exists():
        Usuario.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@burritos.com',
            nombre='Administrador',
            rol='admin'
        )
        print('✅ Admin creado')
    else:
        print('⚠️ Admin ya existe')
except Exception as e:
    print(f'❌ Error: {e}')

try:
    if not Usuario.objects.filter(username='cliente').exists():
        Usuario.objects.create_user(
            username='cliente',
            password='cliente123',
            email='cliente@burritos.com',
            nombre='Cliente Demo',
            rol='cliente'
        )
        print('✅ Cliente creado')
    else:
        print('⚠️ Cliente ya existe')
except Exception as e:
    print(f'❌ Error: {e}')
"""
    
    execute_console_command(
        f'workon burritos_env && cd ~/burritos-to-go-api && python manage.py shell << \'EOFMARKER\'\n{create_admin_script}\nEOFMARKER',
        "Creando usuarios de prueba"
    )
    
    # Paso 11: Recargar webapp
    print_status("Recargando Web App...", 'INFO')
    reload_url = f'{BASE_URL}/webapps/{DOMAIN}/reload/'
    response = make_request('POST', reload_url)
    
    if response and response.status_code == 200:
        print_status("Web App recargada exitosamente", 'SUCCESS')
    else:
        print_status("No se pudo recargar automáticamente, hazlo manualmente", 'WARNING')
    
    # Resumen final
    print_status("=== DEPLOYMENT COMPLETADO ===", 'SUCCESS')
    print(f"""
    🎉 Tu aplicación está desplegada en:
    
    🌐 URL Principal: https://{DOMAIN}
    👤 Admin Panel: https://{DOMAIN}/admin/
    🔧 API Dashboard: https://{DOMAIN}/api/panel/
    📡 API Endpoints: https://{DOMAIN}/api/
    
    📝 Credenciales por defecto:
    
    Admin:
      Usuario: admin
      Contraseña: admin123
    
    Cliente:
      Usuario: cliente
      Contraseña: cliente123
    
    💡 Próximos pasos:
    1. Verifica que la aplicación esté funcionando
    2. Cambia las contraseñas por defecto
    3. Configura HTTPS si es necesario
    4. Revisa los logs en PythonAnywhere si hay errores
    """)
    
    return True

if __name__ == '__main__':
    try:
        deploy_project()
    except KeyboardInterrupt:
        print_status("\nDeployment cancelado por el usuario", 'WARNING')
    except Exception as e:
        print_status(f"Error durante el deployment: {str(e)}", 'ERROR')
        import traceback
        traceback.print_exc()
