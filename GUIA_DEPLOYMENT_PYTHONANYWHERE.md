# 🚀 Guía Completa de Deployment en PythonAnywhere

## 📋 Información del Proyecto

**Proyecto:** Burritos To Go API  
**Repositorio:** https://github.com/BernardoPD/burritos-to-go-api.git  
**Cuenta PythonAnywhere:** pradodiazbackend  
**URL de producción:** https://pradodiazbackend.pythonanywhere.com

---

## 🎯 Opción 1: Deployment Automático (Recomendado)

### Requisitos previos
- Python 3.x instalado localmente
- pip instalado
- Acceso a internet

### Pasos:

1. **Instalar dependencia necesaria:**
```bash
pip install requests
```

2. **Ejecutar el script de deployment:**
```bash
python deploy_pythonanywhere.py
```

3. **Esperar a que termine el proceso** (aproximadamente 5-10 minutos)

4. **Verificar el deployment:**
   - Ir a: https://pradodiazbackend.pythonanywhere.com
   - Admin: https://pradodiazbackend.pythonanywhere.com/admin/
   - API: https://pradodiazbackend.pythonanywhere.com/api/

---

## 🔧 Opción 2: Deployment Manual

### Paso 1: Preparar el repositorio

```bash
# En tu máquina local
cd "D:\prado\UTH 2025-3\APLICACION WEB\Files\U3\burritos_to_go"
git add .
git commit -m "Preparando deployment a PythonAnywhere"
git push origin main
```

### Paso 2: Configurar PythonAnywhere

1. **Iniciar sesión en PythonAnywhere:**
   - URL: https://www.pythonanywhere.com
   - Usuario: pradodiazbackend
   - Contraseña: Fw$*R(STC3eM7M3

2. **Abrir una consola Bash:**
   - Dashboard > Consoles > New Console > Bash

### Paso 3: Clonar el repositorio

```bash
# En la consola de PythonAnywhere
cd ~
git clone https://github.com/BernardoPD/burritos-to-go-api.git
cd burritos-to-go-api
```

### Paso 4: Crear entorno virtual

```bash
mkvirtualenv --python=/usr/bin/python3.11 burritos_env
workon burritos_env
```

### Paso 5: Instalar dependencias

```bash
pip install -r requirements.txt
pip install mysqlclient
```

### Paso 6: Crear base de datos MySQL

1. **Ir a:** Dashboard > Databases
2. **Crear nueva base de datos MySQL:**
   - Nombre: `burritos_db`
   - La base de datos completa será: `pradodiazbackend$burritos_db`

3. **Anotar los datos de conexión:**
   - Host: `pradodiazbackend.mysql.pythonanywhere-services.com`
   - Usuario: `pradodiazbackend`
   - Contraseña: `Fw$*R(STC3eM7M3`

### Paso 7: Configurar settings.py

```bash
cd ~/burritos-to-go-api/burritos_project
nano settings.py
```

**Modificar las siguientes secciones:**

```python
# DEBUG
DEBUG = False

# ALLOWED_HOSTS
ALLOWED_HOSTS = ['pradodiazbackend.pythonanywhere.com', 'www.pradodiazbackend.pythonanywhere.com']

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pradodiazbackend$burritos_db',
        'USER': 'pradodiazbackend',
        'PASSWORD': 'Fw$*R(STC3eM7M3',
        'HOST': 'pradodiazbackend.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

# STATIC FILES
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

### Paso 8: Ejecutar migraciones

```bash
cd ~/burritos-to-go-api
python manage.py migrate
```

### Paso 9: Crear superusuario

```bash
python manage.py createsuperuser
# Usuario: admin
# Email: admin@burritos.com
# Contraseña: admin123
```

### Paso 10: Colectar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

### Paso 11: Configurar Web App

1. **Ir a:** Dashboard > Web
2. **Click en:** Add a new web app
3. **Seleccionar:** Manual configuration
4. **Python version:** 3.11

5. **Configurar WSGI file:**
   - Click en el archivo WSGI
   - Reemplazar todo el contenido con:

```python
import os
import sys

# Agregar el proyecto al path
path = '/home/pradodiazbackend/burritos-to-go-api'
if path not in sys.path:
    sys.path.append(path)

# Configurar Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'

# Importar la aplicación WSGI de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. **Configurar Virtualenv:**
   - En la sección "Virtualenv"
   - Path: `/home/pradodiazbackend/.virtualenvs/burritos_env`

7. **Configurar Static files:**
   - URL: `/static/`
   - Directory: `/home/pradodiazbackend/burritos-to-go-api/static`

8. **Click en:** Reload

---

## ✅ Verificación del Deployment

### 1. Verificar que la aplicación funciona:
```
https://pradodiazbackend.pythonanywhere.com
```

### 2. Verificar el admin:
```
https://pradodiazbackend.pythonanywhere.com/admin/
Usuario: admin
Contraseña: admin123
```

### 3. Verificar las APIs:
```
https://pradodiazbackend.pythonanywhere.com/api/
https://pradodiazbackend.pythonanywhere.com/api/panel/
```

### 4. Probar endpoints principales:
- `GET /api/menu/` - Lista de productos
- `POST /api/pedidos/` - Crear pedido (requiere autenticación)
- `GET /api/mis-pedidos/` - Ver pedidos del cliente
- `POST /api/recargar-saldo/` - Recargar saldo

---

## 🔍 Solución de Problemas

### Error 500 - Internal Server Error

1. **Ver logs de error:**
   - Dashboard > Web > Log files > Error log

2. **Ver logs de servidor:**
   - Dashboard > Web > Log files > Server log

3. **Verificar configuración:**
```bash
cd ~/burritos-to-go-api
workon burritos_env
python manage.py check
```

### Error de base de datos

```bash
# Verificar conexión a la base de datos
python manage.py dbshell
```

### Error de permisos

```bash
# Verificar permisos de archivos
cd ~/burritos-to-go-api
chmod -R 755 .
```

### Actualizar código después de cambios

```bash
cd ~/burritos-to-go-api
git pull origin main
workon burritos_env
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Luego recargar la webapp desde el dashboard.

---

## 📡 Endpoints Disponibles

### Autenticación
- `POST /api/token/` - Obtener token de autenticación
- `POST /api/login/` - Login alternativo

### Cliente
- `GET /api/menu/` - Ver menú de productos
- `POST /api/pedidos/` - Crear nuevo pedido
- `GET /api/mis-pedidos/` - Ver mis pedidos
- `GET /api/pedido/<id>/` - Ver detalle de pedido
- `POST /api/recargar-saldo/` - Recargar saldo
- `GET /api/mi-saldo/` - Consultar saldo actual
- `GET /api/panel/` - Dashboard del cliente

### Administrador
- `GET /api/productos/` - Lista de productos (CRUD)
- `GET /api/pedidos-admin/` - Lista de todos los pedidos
- `GET /api/usuarios/` - Lista de usuarios (CRUD)

---

## 🔐 Seguridad

### Cambiar contraseñas por defecto:

```bash
cd ~/burritos-to-go-api
workon burritos_env
python manage.py changepassword admin
python manage.py changepassword cliente
```

### Generar nueva SECRET_KEY:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copiar la nueva key y actualizarla en `settings.py`.

---

## 📱 Integración con Flutter

### URL Base para Flutter:
```dart
const String BASE_URL = 'https://pradodiazbackend.pythonanywhere.com/api/';
```

### Headers requeridos:
```dart
{
  'Content-Type': 'application/json',
  'Authorization': 'Token <token_del_usuario>'
}
```

### Ejemplo de petición:
```dart
final response = await http.get(
  Uri.parse('$BASE_URL/menu/'),
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Token $userToken',
  },
);
```

---

## 📞 Soporte

**Credenciales de PythonAnywhere:**
- Usuario: pradodiazbackend
- Contraseña: Fw$*R(STC3eM7M3
- API Token: 4b299407e0f84fd583a1aa029676fe51884b1b48

**Repositorio:**
- https://github.com/BernardoPD/burritos-to-go-api

---

## 📝 Notas Importantes

1. ✅ La base de datos se migra automáticamente
2. ✅ Los usuarios admin y cliente se crean automáticamente
3. ✅ Todos los endpoints están listos para consumir
4. ✅ CORS está configurado para aceptar todas las origins
5. ⚠️ Cambiar DEBUG=False en producción
6. ⚠️ Cambiar SECRET_KEY en producción
7. ⚠️ Cambiar contraseñas por defecto

---

## 🎉 ¡Listo!

Tu aplicación Burritos To Go está desplegada y lista para ser consumida por el frontend Flutter.

**URL Principal:** https://pradodiazbackend.pythonanywhere.com
