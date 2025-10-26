# 🚀 Guía Completa de Deployment en PythonAnywhere
## Burritos To Go API

---

## 📋 Tabla de Contenidos
1. [Preparativos Antes de Deployment](#preparativos-antes-de-deployment)
2. [Paso a Paso Manual](#paso-a-paso-manual)
3. [Configuración de Base de Datos](#configuración-de-base-de-datos)
4. [Configuración de Archivos Estáticos](#configuración-de-archivos-estáticos)
5. [Configuración de WSGI](#configuración-de-wsgi)
6. [Migraciones y Datos Iniciales](#migraciones-y-datos-iniciales)
7. [Pruebas Finales](#pruebas-finales)
8. [Solución de Problemas](#solución-de-problemas)

---

## ✅ Preparativos Antes de Deployment

### 1. Cuenta de PythonAnywhere
- **Usuario:** `pradodiazbackend`
- **Password:** `Fw$*R(STC3eM7M3`
- **URL:** https://www.pythonanywhere.com/user/pradodiazbackend/

### 2. Repositorio en GitHub
- **URL:** https://github.com/BernardoPD/burritos-to-go-api
- El código ya está subido y listo para clonar

### 3. Token de API (si se necesita)
```
Token: 4b299407e0f84fd583a1aa029676fe51884b1b48
```

---

## 📝 Paso a Paso Manual

### PASO 1: Clonar Repositorio

1. Inicia sesión en PythonAnywhere: https://www.pythonanywhere.com/login/

2. Ve a **"Consoles"** → **"Bash"**

3. Clona el repositorio:
```bash
cd ~
git clone https://github.com/BernardoPD/burritos-to-go-api.git
cd burritos-to-go-api
```

---

### PASO 2: Crear Entorno Virtual

```bash
# Crear entorno virtual con Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 burritosenv

# Activar entorno (se activa automáticamente al crearlo)
# Si necesitas activarlo manualmente:
workon burritosenv
```

---

### PASO 3: Instalar Dependencias

```bash
# Asegúrate de estar en el directorio del proyecto
cd ~/burritos-to-go-api

# Instalar dependencias
pip install -r requirements.txt

# Si requirements.txt no tiene mysqlclient, instalarlo:
pip install mysqlclient
```

**Contenido de requirements.txt:**
```
Django==5.2
djangorestframework==3.15.2
django-cors-headers==4.6.0
requests
mysqlclient
```

---

### PASO 4: Configurar Base de Datos MySQL

#### 4.1 Crear Base de Datos en PythonAnywhere

1. Ve a **"Databases"** en el menú superior

2. En **"Create a database"**, ingresa:
   - **Database name:** `pradodiazbackend$burritos_db`
   - Click en **"Create"**

3. Anota la información de conexión:
   - **Host:** `pradodiazbackend.mysql.pythonanywhere-services.com`
   - **Username:** `pradodiazbackend`
   - **Database:** `pradodiazbackend$burritos_db`
   - **Password:** El que configuraste en PythonAnywhere

#### 4.2 Crear Contraseña de MySQL (si no existe)

1. En la sección **"Databases"**, ve a **"MySQL password"**
2. Configura una contraseña segura (ejemplo: `MysqlPass123!`)
3. **IMPORTANTE:** Anota esta contraseña

---

### PASO 5: Configurar settings.py

```bash
# Editar settings.py
nano ~/burritos-to-go-api/burritos_project/settings.py
```

**Modificar las siguientes secciones:**

```python
# SEGURIDAD
DEBUG = False  # ⚠️ IMPORTANTE: False en producción

ALLOWED_HOSTS = ['pradodiazbackend.pythonanywhere.com']

# BASE DE DATOS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pradodiazbackend$burritos_db',
        'USER': 'pradodiazbackend',
        'PASSWORD': 'MysqlPass123!',  # Tu contraseña de MySQL
        'HOST': 'pradodiazbackend.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# ARCHIVOS ESTÁTICOS
STATIC_URL = '/static/'
STATIC_ROOT = '/home/pradodiazbackend/burritos-to-go-api/staticfiles'

# CORS (si es necesario para Flutter)
CORS_ALLOW_ALL_ORIGINS = True  # Solo para desarrollo
# En producción, especifica dominios:
# CORS_ALLOWED_ORIGINS = [
#     "https://tu-app-flutter.com",
# ]
```

**Guardar:** `Ctrl + O` → `Enter` → `Ctrl + X`

---

### PASO 6: Aplicar Migraciones

```bash
# Asegúrate de que el entorno virtual esté activo
workon burritosenv

cd ~/burritos-to-go-api

# Crear migraciones (si no existen)
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

---

### PASO 7: Crear Superusuario

```bash
python manage.py createsuperuser

# Ingresa:
# Username: admin
# Email: admin@burritos.com
# Password: admin123  (o tu password preferido)
```

---

### PASO 8: Colectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

---

### PASO 9: Crear Web App en PythonAnywhere

1. Ve a **"Web"** en el menú superior

2. Click en **"Add a new web app"**

3. Selecciona tu dominio:
   - `pradodiazbackend.pythonanywhere.com`

4. Selecciona **"Manual configuration"** (no "Django")

5. Selecciona **Python 3.10**

6. Click **"Next"**

---

### PASO 10: Configurar WSGI

1. En la página **"Web"**, scroll down a **"Code"**

2. Click en el link del archivo **WSGI configuration file**

3. **Reemplaza TODO** el contenido con:

```python
import os
import sys

# Ruta al proyecto
path = '/home/pradodiazbackend/burritos-to-go-api'
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar variable de entorno de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'

# Cargar aplicación Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. Guarda el archivo: **"Save"** (botón verde arriba)

---

### PASO 11: Configurar Virtualenv en Web App

1. En la página **"Web"**, ve a la sección **"Virtualenv"**

2. En **"Enter path to a virtualenv"**, ingresa:
   ```
   /home/pradodiazbackend/.virtualenvs/burritosenv
   ```

3. Click **"✓"** (checkmark)

---

### PASO 12: Configurar Archivos Estáticos

1. En la página **"Web"**, scroll a **"Static files"**

2. Agrega la siguiente entrada:
   - **URL:** `/static/`
   - **Directory:** `/home/pradodiazbackend/burritos-to-go-api/staticfiles`

3. Click en **"✓"** (checkmark)

---

### PASO 13: Recargar Web App

1. En la página **"Web"**, scroll arriba

2. Click en el botón verde **"Reload pradodiazbackend.pythonanywhere.com"**

3. Espera unos segundos

---

### PASO 14: Poblar Base de Datos con Datos de Prueba

```bash
# Desde la consola Bash
workon burritosenv
cd ~/burritos-to-go-api

# Abrir shell de Django
python manage.py shell
```

**Dentro del shell de Python:**

```python
from core.models import Usuario, Categoria, Producto, Pedido
from decimal import Decimal

# Crear categorías
cat_burritos = Categoria.objects.create(nombre='Burritos')
cat_bebidas = Categoria.objects.create(nombre='Bebidas')
cat_extras = Categoria.objects.create(nombre='Extras')

# Crear productos
Producto.objects.create(
    nombre='Burrito de Carne',
    descripcion='Delicioso burrito con carne asada, frijoles y queso',
    precio=Decimal('80.00'),
    categoria=cat_burritos,
    activo=True
)

Producto.objects.create(
    nombre='Burrito de Pollo',
    descripcion='Burrito con pollo a la parrilla y vegetales',
    precio=Decimal('75.00'),
    categoria=cat_burritos,
    activo=True
)

Producto.objects.create(
    nombre='Burrito Vegetariano',
    descripcion='Burrito con vegetales frescos y guacamole',
    precio=Decimal('70.00'),
    categoria=cat_burritos,
    activo=True
)

Producto.objects.create(
    nombre='Refresco',
    descripcion='Refresco de 500ml',
    precio=Decimal('20.00'),
    categoria=cat_bebidas,
    activo=True
)

Producto.objects.create(
    nombre='Agua',
    descripcion='Agua purificada de 600ml',
    precio=Decimal('15.00'),
    categoria=cat_bebidas,
    activo=True
)

Producto.objects.create(
    nombre='Papas Fritas',
    descripcion='Papas fritas crujientes',
    precio=Decimal('30.00'),
    categoria=cat_extras,
    activo=True
)

# Crear usuario cliente de prueba
cliente = Usuario.objects.create_user(
    username='cliente',
    email='cliente@example.com',
    password='cliente123',
    rol='cliente',
    saldo=Decimal('500.00'),
    first_name='Juan',
    last_name='Pérez'
)

print("✅ Datos de prueba creados exitosamente")

# Salir del shell
exit()
```

---

## 🧪 Pruebas Finales

### 1. Verificar API en Navegador

Abre en tu navegador:
```
https://pradodiazbackend.pythonanywhere.com/api/
```

Deberías ver la interfaz de Django REST Framework.

### 2. Probar Endpoints

#### Login de Cliente:
```bash
curl -X POST https://pradodiazbackend.pythonanywhere.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"cliente","password":"cliente123"}'
```

**Respuesta esperada:**
```json
{
  "mensaje": "Login exitoso",
  "token": "abc123...",
  "usuario": {
    "username": "cliente",
    "saldo": 500.00,
    ...
  }
}
```

#### Consultar Menú:
```bash
curl https://pradodiazbackend.pythonanywhere.com/api/cliente/menu/
```

#### Consultar Saldo (requiere token):
```bash
curl -X GET https://pradodiazbackend.pythonanywhere.com/api/cliente/mi-saldo/ \
  -H "Authorization: Token TU_TOKEN_AQUI"
```

### 3. Acceder al Admin

```
https://pradodiazbackend.pythonanywhere.com/admin/
```

- **Usuario:** admin
- **Password:** admin123 (el que creaste)

---

## 🛠️ Solución de Problemas

### Error: "DisallowedHost at /"

**Solución:** Verifica que `ALLOWED_HOSTS` en `settings.py` incluya tu dominio:
```python
ALLOWED_HOSTS = ['pradodiazbackend.pythonanywhere.com']
```

Luego recarga la web app.

---

### Error: "No module named 'core'"

**Solución:** Verifica la configuración del WSGI:
```python
# En el archivo WSGI, asegúrate de que la ruta sea correcta:
path = '/home/pradodiazbackend/burritos-to-go-api'
```

---

### Error: "OperationalError: (2003, "Can't connect to MySQL server")"

**Solución:**
1. Verifica que la base de datos existe en PythonAnywhere → Databases
2. Verifica las credenciales en `settings.py`:
   - `NAME`: `pradodiazbackend$burritos_db`
   - `USER`: `pradodiazbackend`
   - `PASSWORD`: Tu contraseña de MySQL
   - `HOST`: `pradodiazbackend.mysql.pythonanywhere-services.com`

---

### Error 500 - Internal Server Error

**Solución:**
1. Ve a **"Web"** → **"Log files"**
2. Abre **"Error log"**
3. Lee el último error para identificar el problema
4. Los errores comunes:
   - Módulo no encontrado → Instalar con `pip install`
   - Error de sintaxis → Revisar código
   - Error de base de datos → Revisar configuración

---

### Los archivos estáticos no se muestran

**Solución:**
```bash
# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

Verifica configuración en Web → Static files:
- URL: `/static/`
- Directory: `/home/pradodiazbackend/burritos-to-go-api/staticfiles`

---

### Cambios no se reflejan

**Solución:**
1. Siempre recarga la web app después de hacer cambios
2. En **"Web"**, click en **"Reload"** (botón verde)

---

## 📱 URLs Finales para Flutter

```dart
class ApiConfig {
  // URL base de producción
  static const String baseUrl = 'https://pradodiazbackend.pythonanywhere.com/api/';
  
  // Endpoints principales
  static const String login = '${baseUrl}auth/login/';
  static const String register = '${baseUrl}auth/register/';
  static const String menu = '${baseUrl}cliente/menu/';
  static const String misPedidos = '${baseUrl}cliente/mis-pedidos/';
  static const String miSaldo = '${baseUrl}cliente/mi-saldo/';
  static const String recargarSaldo = '${baseUrl}cliente/recargar-saldo/';
  static const String crearPedido = '${baseUrl}pedidos/';
}
```

---

## ✅ Checklist Final

- [ ] Repositorio clonado en PythonAnywhere
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] Base de datos MySQL creada
- [ ] `settings.py` configurado correctamente
- [ ] Migraciones aplicadas
- [ ] Superusuario creado
- [ ] Archivos estáticos colectados
- [ ] Web App creada
- [ ] WSGI configurado
- [ ] Virtualenv configurado en Web App
- [ ] Archivos estáticos configurados en Web App
- [ ] Web App recargada
- [ ] Datos de prueba insertados
- [ ] API funcionando correctamente
- [ ] Admin accesible

---

## 📞 Información de Acceso

### PythonAnywhere
- **URL:** https://www.pythonanywhere.com/user/pradodiazbackend/
- **Usuario:** pradodiazbackend
- **Password:** Fw$*R(STC3eM7M3

### API en Producción
- **Base URL:** https://pradodiazbackend.pythonanywhere.com/api/
- **Admin Panel:** https://pradodiazbackend.pythonanywhere.com/admin/
- **Cliente Dashboard:** https://pradodiazbackend.pythonanywhere.com/api/panel/

### Credenciales de Prueba
- **Admin:** admin / admin123
- **Cliente:** cliente / cliente123

---

## 🔄 Actualizar Código en el Futuro

```bash
# Conectar a Bash console
cd ~/burritos-to-go-api

# Activar entorno virtual
workon burritosenv

# Actualizar desde GitHub
git pull origin main

# Instalar nuevas dependencias (si hay)
pip install -r requirements.txt

# Aplicar nuevas migraciones (si hay)
python manage.py migrate

# Colectar archivos estáticos
python manage.py collectstatic --noinput

# IMPORTANTE: Recargar web app
# Ve a Web → Reload
```

---

**Última actualización:** 2025-10-26  
**Desarrollador:** Bernardo Prado  
**Repositorio:** https://github.com/BernardoPD/burritos-to-go-api
