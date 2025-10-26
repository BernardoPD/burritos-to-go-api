# 🚀 Deployment Paso a Paso en PythonAnywhere

## ✅ Código ya subido a GitHub
El código está disponible en: https://github.com/BernardoPD/burritos-to-go-api.git

---

## 📋 Paso 1: Acceder a PythonAnywhere

1. Ve a: **https://www.pythonanywhere.com/login/**
2. Inicia sesión con:
   - **Username:** pradodiazbackend
   - **Password:** Fw$*R(STC3eM7M3

---

## 💾 Paso 2: Crear Base de Datos MySQL

1. En el dashboard, click en la pestaña **"Databases"**
2. En la sección **"Create a new database"**:
   - Nombre: `burritos_db`
   - Click en **"Create"**

3. Anota los siguientes datos (aparecen en la página):
   ```
   Host: pradodiazbackend.mysql.pythonanywhere-services.com
   Username: pradodiazbackend
   Database name: pradodiazbackend$burritos_db
   Password: Fw$*R(STC3eM7M3
   ```

---

## 🖥️ Paso 3: Abrir Consola Bash

1. Click en la pestaña **"Consoles"**
2. Click en **"Bash"** (dentro de "Start a new console")
3. Se abrirá una terminal negra

---

## 📥 Paso 4: Clonar el Repositorio

En la consola bash que acabas de abrir, copia y pega estos comandos uno por uno:

```bash
cd ~
```

```bash
git clone https://github.com/BernardoPD/burritos-to-go-api.git
```

```bash
cd burritos-to-go-api
```

```bash
ls -la
```

Deberías ver los archivos del proyecto.

---

## 🐍 Paso 5: Crear Entorno Virtual

```bash
mkvirtualenv --python=/usr/bin/python3.11 burritos_env
```

Espera a que termine (aparecerá `(burritos_env)` al inicio de la línea).

---

## 📦 Paso 6: Instalar Dependencias

```bash
workon burritos_env
```

```bash
pip install django==5.2
```

```bash
pip install djangorestframework==3.15.2
```

```bash
pip install django-cors-headers==4.6.0
```

```bash
pip install mysqlclient
```

Espera a que cada comando termine antes de ejecutar el siguiente.

---

## ⚙️ Paso 7: Configurar settings.py

```bash
cd ~/burritos-to-go-api/burritos_project
```

```bash
nano settings.py
```

Esto abrirá un editor de texto. Busca y modifica estas líneas:

### 7.1 Cambiar DEBUG (línea 26):
```python
DEBUG = False
```

### 7.2 Cambiar ALLOWED_HOSTS (línea 28):
```python
ALLOWED_HOSTS = ['pradodiazbackend.pythonanywhere.com']
```

### 7.3 Cambiar DATABASES (línea 80-92):
```python
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
```

### 7.4 Agregar al FINAL del archivo (después de la línea 143):
```python

# Static files configuration for production
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

### 7.5 Guardar y salir:
- Presiona: `Ctrl + X`
- Presiona: `Y` (para confirmar)
- Presiona: `Enter` (para guardar)

---

## 🗄️ Paso 8: Migrar Base de Datos

```bash
cd ~/burritos-to-go-api
```

```bash
python manage.py migrate
```

Deberías ver muchas líneas que dicen "Applying..." - esto es normal.

---

## 👤 Paso 9: Crear Usuarios

### 9.1 Abrir shell de Django:
```bash
python manage.py shell
```

### 9.2 Copiar y pegar TODO este bloque de una vez:
```python
from core.models import Usuario

# Crear usuario admin
try:
    admin = Usuario.objects.create_superuser(
        username='admin',
        password='admin123',
        email='admin@burritos.com',
        nombre='Administrador',
        rol='admin',
        saldo=0
    )
    print('✅ Admin creado')
except:
    print('⚠️ Admin ya existe')

# Crear usuario cliente
try:
    cliente = Usuario.objects.create_user(
        username='cliente',
        password='cliente123',
        email='cliente@burritos.com',
        nombre='Cliente Demo',
        rol='cliente',
        saldo=500
    )
    print('✅ Cliente creado con saldo de $500')
except:
    print('⚠️ Cliente ya existe')

# Crear algunos productos de ejemplo
from core.models import Producto

productos = [
    {'nombre': 'Burrito de Carne', 'descripcion': 'Delicioso burrito con carne de res', 'precio': 75.00},
    {'nombre': 'Burrito de Pollo', 'descripcion': 'Burrito con pollo marinado', 'precio': 65.00},
    {'nombre': 'Quesadilla', 'descripcion': 'Quesadilla con queso fundido', 'precio': 45.00},
    {'nombre': 'Tacos (3 pzs)', 'descripcion': 'Tres tacos a elegir', 'precio': 55.00},
]

for p in productos:
    try:
        Producto.objects.create(**p, disponible=True)
        print(f'✅ Producto creado: {p["nombre"]}')
    except:
        print(f'⚠️ Producto ya existe: {p["nombre"]}')

print('\n🎉 ¡Setup completado!')
```

### 9.3 Salir del shell:
```python
exit()
```

---

## 📁 Paso 10: Colectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

---

## 🌐 Paso 11: Configurar Web App

1. Ve a la pestaña **"Web"** en el dashboard
2. Click en **"Add a new web app"**
3. Click en **"Next"** (para confirmar el dominio)
4. Selecciona **"Manual configuration"**
5. Selecciona **"Python 3.11"**
6. Click en **"Next"**

---

## 📝 Paso 12: Configurar Virtualenv

En la sección **"Virtualenv"**:

1. Click en **"Enter path to a virtualenv"**
2. Escribe:
   ```
   /home/pradodiazbackend/.virtualenvs/burritos_env
   ```
3. Click en la palomita (✓) para guardar

---

## 🔧 Paso 13: Configurar WSGI

1. En la sección **"Code"**, click en el enlace del archivo WSGI:
   - Dice algo como: `/var/www/pradodiazbackend_pythonanywhere_com_wsgi.py`

2. **BORRA TODO** el contenido del archivo

3. **Copia y pega** este código:

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

4. Click en **"Save"** (botón verde arriba a la derecha)

---

## 📂 Paso 14: Configurar Static Files

En la sección **"Static files"**:

1. Click en **"Enter URL"** y escribe:
   ```
   /static/
   ```

2. Click en **"Enter path"** y escribe:
   ```
   /home/pradodiazbackend/burritos-to-go-api/static
   ```

3. Click en la palomita (✓) para guardar

---

## 🔄 Paso 15: Recargar la Aplicación

1. Scroll hasta arriba de la página
2. Click en el botón verde grande que dice **"Reload pradodiazbackend.pythonanywhere.com"**
3. Espera 5-10 segundos

---

## ✅ Paso 16: Verificar que Funciona

Abre en tu navegador:

### 1. Página principal:
```
https://pradodiazbackend.pythonanywhere.com/api/
```
Deberías ver la interfaz del Django REST Framework.

### 2. Panel de administración:
```
https://pradodiazbackend.pythonanywhere.com/admin/
```
- Usuario: `admin`
- Contraseña: `admin123`

### 3. Dashboard de cliente:
```
https://pradodiazbackend.pythonanywhere.com/api/panel/
```
- Usuario: `cliente`
- Contraseña: `cliente123`

---

## 🎯 URLs de la API para Flutter

```dart
const String BASE_URL = 'https://pradodiazbackend.pythonanywhere.com/api/';
```

### Endpoints principales:

**Autenticación:**
- `POST /api/token/` - Obtener token

**Cliente:**
- `GET /api/menu/` - Ver menú
- `GET /api/mi-saldo/` - Ver saldo
- `POST /api/recargar-saldo/` - Recargar saldo
- `POST /api/pedidos/` - Crear pedido
- `GET /api/mis-pedidos/` - Ver mis pedidos
- `GET /api/pedido/<id>/` - Detalle de pedido

**Admin:**
- `GET /api/productos/` - Gestionar productos
- `GET /api/pedidos-admin/` - Ver todos los pedidos
- `GET /api/usuarios/` - Gestionar usuarios

---

## 🔍 Solución de Problemas

### Si ves un error 500:

1. Ve a la pestaña **"Web"**
2. Scroll hasta **"Log files"**
3. Click en **"error.log"**
4. Lee los últimos errores (están al final del archivo)

### Si la página no carga:

1. Verifica que el botón "Reload" esté verde
2. Espera 1 minuto y vuelve a intentar
3. Verifica que todos los pasos se hayan completado

### Si no puedes iniciar sesión:

Vuelve a la consola Bash y ejecuta:
```bash
cd ~/burritos-to-go-api
python manage.py shell
```

Luego:
```python
from core.models import Usuario
Usuario.objects.create_superuser(username='admin', password='admin123', email='admin@test.com', nombre='Admin', rol='admin')
exit()
```

---

## 📱 Para el Equipo de Flutter

Envíales este documento:
- **GUIA_FLUTTER_INTEGRACION.md**

Y estas credenciales de prueba:
```
URL Base: https://pradodiazbackend.pythonanywhere.com/api/

Cliente de prueba:
  username: cliente
  password: cliente123
  saldo inicial: $500

Admin de prueba:
  username: admin
  password: admin123
```

---

## 🎉 ¡Listo!

Tu aplicación está desplegada en:
**https://pradodiazbackend.pythonanywhere.com**

Todos los endpoints están funcionando y listos para ser consumidos por Flutter.

---

## 📞 Credenciales PythonAnywhere

Para futuras actualizaciones:
- **URL:** https://www.pythonanywhere.com
- **Usuario:** pradodiazbackend
- **Contraseña:** Fw$*R(STC3eM7M3
- **API Token:** 4b299407e0f84fd583a1aa029676fe51884b1b48

### Para actualizar el código después de cambios:

```bash
cd ~/burritos-to-go-api
git pull origin main
workon burritos_env
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Luego click en "Reload" en la pestaña Web.
