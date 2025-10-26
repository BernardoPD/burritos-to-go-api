# ⚡ INSTRUCCIONES RÁPIDAS - DEPLOYMENT MANUAL

## 🎯 OBJETIVO
Desplegar la API de Burritos To Go en PythonAnywhere manualmente.

---

## 📝 PASO A PASO SIMPLIFICADO

### 1️⃣ ACCEDER A PYTHONANYWHERE

Ve a: **https://www.pythonanywhere.com/login/**

Credenciales:
- Usuario: `pradodiazbackend`
- Password: `Fw$*R(STC3eM7M3`

---

### 2️⃣ CREAR BASE DE DATOS

1. Click en pestaña **"Databases"**
2. En "Create a new database", escribe: `burritos_db`
3. Click **"Create"**

---

### 3️⃣ ABRIR CONSOLA BASH

1. Click en pestaña **"Consoles"**
2. Click en **"Bash"**

---

### 4️⃣ CLONAR REPOSITORIO

Copia y pega estos comandos (uno por uno):

```bash
cd ~
```

```bash
git clone https://github.com/BernardoPD/burritos-to-go-api.git
```

```bash
cd burritos-to-go-api
```

---

### 5️⃣ CREAR ENTORNO VIRTUAL

```bash
mkvirtualenv --python=/usr/bin/python3.11 burritos_env
```

Espera a que aparezca `(burritos_env)` al inicio de la línea.

---

### 6️⃣ INSTALAR DEPENDENCIAS

```bash
workon burritos_env
```

```bash
pip install django==5.2 djangorestframework==3.15.2 django-cors-headers==4.6.0 mysqlclient
```

---

### 7️⃣ CONFIGURAR SETTINGS

```bash
cd ~/burritos-to-go-api/burritos_project
```

```bash
nano settings.py
```

**Cambia estas líneas:**

Línea 26:
```python
DEBUG = False
```

Línea 28:
```python
ALLOWED_HOSTS = ['pradodiazbackend.pythonanywhere.com']
```

Líneas 80-92 (reemplaza todo el bloque DATABASES):
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

Al final del archivo (después de línea 143), agrega:
```python

import os
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

**Guardar:**
- `Ctrl + X`
- `Y`
- `Enter`

---

### 8️⃣ MIGRAR BASE DE DATOS

```bash
cd ~/burritos-to-go-api
```

```bash
python manage.py migrate
```

---

### 9️⃣ CREAR USUARIOS Y DATOS

```bash
python manage.py shell
```

Copia y pega TODO este bloque:

```python
from core.models import Usuario, Producto

# Crear admin
try:
    Usuario.objects.create_superuser(username='admin', password='admin123', email='admin@test.com', nombre='Admin', rol='admin', saldo=0)
    print('✅ Admin creado')
except: print('⚠️ Admin ya existe')

# Crear cliente
try:
    Usuario.objects.create_user(username='cliente', password='cliente123', email='cliente@test.com', nombre='Cliente Demo', rol='cliente', saldo=500)
    print('✅ Cliente creado')
except: print('⚠️ Cliente ya existe')

# Crear productos
productos = [
    {'nombre': 'Burrito de Carne', 'descripcion': 'Burrito con carne', 'precio': 75.00},
    {'nombre': 'Burrito de Pollo', 'descripcion': 'Burrito con pollo', 'precio': 65.00},
    {'nombre': 'Quesadilla', 'descripcion': 'Quesadilla de queso', 'precio': 45.00},
    {'nombre': 'Tacos (3 pzs)', 'descripcion': 'Tres tacos', 'precio': 55.00},
]

for p in productos:
    try:
        Producto.objects.create(**p, disponible=True)
        print(f'✅ {p["nombre"]}')
    except: pass

print('🎉 Listo!')
exit()
```

---

### 🔟 COLECTAR ARCHIVOS ESTÁTICOS

```bash
python manage.py collectstatic --noinput
```

---

### 1️⃣1️⃣ CONFIGURAR WEB APP

1. Ve a pestaña **"Web"**
2. Click **"Add a new web app"**
3. Click **"Next"**
4. Selecciona **"Manual configuration"**
5. Selecciona **"Python 3.11"**
6. Click **"Next"**

---

### 1️⃣2️⃣ CONFIGURAR VIRTUALENV

En sección "Virtualenv":
1. Click en "Enter path to a virtualenv"
2. Escribe: `/home/pradodiazbackend/.virtualenvs/burritos_env`
3. Click ✓

---

### 1️⃣3️⃣ CONFIGURAR WSGI

1. En sección "Code", click en el archivo WSGI
2. **BORRA TODO** el contenido
3. Pega esto:

```python
import os
import sys

path = '/home/pradodiazbackend/burritos-to-go-api'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. Click **"Save"**

---

### 1️⃣4️⃣ CONFIGURAR STATIC FILES

En sección "Static files":
1. URL: `/static/`
2. Path: `/home/pradodiazbackend/burritos-to-go-api/static`
3. Click ✓

---

### 1️⃣5️⃣ RECARGAR APP

Click en botón verde **"Reload pradodiazbackend.pythonanywhere.com"**

---

## ✅ VERIFICAR

Abre en tu navegador:

**API:**
```
https://pradodiazbackend.pythonanywhere.com/api/
```

**Admin:**
```
https://pradodiazbackend.pythonanywhere.com/admin/
Usuario: admin
Password: admin123
```

**Dashboard Cliente:**
```
https://pradodiazbackend.pythonanywhere.com/api/panel/
Usuario: cliente
Password: cliente123
```

---

## 🎉 ¡LISTO!

Tu API está desplegada en:
**https://pradodiazbackend.pythonanywhere.com**

---

## 📱 PARA FLUTTER

URL Base:
```dart
const String BASE_URL = 'https://pradodiazbackend.pythonanywhere.com/api/';
```

Credenciales de prueba:
```
Username: cliente
Password: cliente123
```

---

## 🔄 ACTUALIZAR DESPUÉS DE CAMBIOS

```bash
cd ~/burritos-to-go-api
git pull origin main
workon burritos_env
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Luego click en "Reload" en pestaña Web.

---

## 📞 AYUDA

Si algo falla, ve a:
- Web tab > Log files > Error log

Lee: `DEPLOYMENT_PASO_A_PASO.md` para más detalles.
