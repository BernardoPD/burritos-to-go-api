"""
WSGI config for PythonAnywhere deployment.

INSTRUCCIONES:
1. Ve a la pestaña "Web" en PythonAnywhere
2. Click en "Add a new web app"
3. Selecciona Python 3.10
4. Selecciona "Manual configuration"
5. En la sección "Code", edita el archivo WSGI
6. Reemplaza TODO el contenido con este archivo
7. IMPORTANTE: Cambia 'TU_USUARIO' por tu nombre de usuario de PythonAnywhere
"""

import os
import sys

# Añadir el directorio del proyecto al path
# CAMBIAR 'TU_USUARIO' por tu nombre de usuario de PythonAnywhere
path = '/home/TU_USUARIO/burritos_to_go'
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar el módulo de settings de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'

# Configurar Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
