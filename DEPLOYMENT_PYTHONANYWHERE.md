# 🚀 Guía de Deployment en PythonAnywhere

## Tabla de Contenidos
- [Requisitos Previos](#requisitos-previos)
- [Paso 1: Crear Cuenta](#paso-1-crear-cuenta-en-pythonanywhere)
- [Paso 2: Clonar Repositorio](#paso-2-clonar-el-repositorio)
- [Paso 3: Crear Entorno Virtual](#paso-3-crear-entorno-virtual)
- [Paso 4: Instalar Dependencias](#paso-4-instalar-dependencias)
- [Paso 5: Configurar Settings](#paso-5-configurar-settings)
- [Paso 6: Migrar Base de Datos](#paso-6-migrar-base-de-datos)
- [Paso 7: Copiar Datos Locales](#paso-7-copiar-datos-locales-a-pythonanywhere)
- [Paso 8: Configurar Archivos Estáticos](#paso-8-configurar-archivos-estáticos)
- [Paso 9: Configurar Web App](#paso-9-configurar-web-app)
- [Paso 10: Verificar Funcionamiento](#paso-10-verificar-funcionamiento)
- [Troubleshooting](#troubleshooting)

---

## Requisitos Previos

✅ Cuenta en PythonAnywhere (free o paid)  
✅ Repositorio en GitHub: https://github.com/BernardoPD/burritos-to-go-api  
✅ Base de datos local funcionando (`db.sqlite3`)

---

## Paso 1: Crear Cuenta en PythonAnywhere

### 1.1 Registro

1. Ve a: **https://www.pythonanywhere.com**
2. Click en **"Start running Python online in less than a minute!"**
3. Elige el plan **Beginner (Free)** o **Hacker ($5/mes)**
4. Completa el registro con tu email

### 1.2 Obtener API Token

1. Inicia sesión en PythonAnywhere
2. Ve a: **Account** → **API Token**
3. Click en **"Create a new API token"**
4. Guarda el token generado

---

## Paso 2: Clonar el Repositorio

### 2.1 Abrir Bash Console

1. En PythonAnywhere, ve a la pestaña **Consoles**
2. Click en **"Bash"**

### 2.2 Clonar desde GitHub

```bash
# Clonar el repositorio
git clone https://github.com/BernardoPD/burritos-to-go-api.git

# Entrar al directorio
cd burritos-to-go-api

# Verificar que se clonó correctamente
ls -la
```

**Resultado esperado:**
```
burritos_project/
core/
manage.py
requirements.txt
README.md
...
```

---

## Paso 3: Crear Entorno Virtual

```bash
# Crear entorno virtual con Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 burritos_env

# Verificar que esté activo (verás (burritos_env) en el prompt)
which python
```

**Nota:** Si necesitas activarlo después:
```bash
workon burritos_env
```

---

## Paso 4: Instalar Dependencias

```bash
# Asegúrate de estar en el entorno virtual (burritos_env)
# y en el directorio del proyecto

pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

**Deberías ver:**
- Django==5.2
- djangorestframework==3.15.2
- django-cors-headers==4.6.0

---

## Paso 5: Configurar Settings

### 5.1 Crear archivo de configuración de producción

```bash
nano burritos_project/settings.py
```

### 5.2 Modificar las siguientes líneas:

**Busca y modifica:**

```python
# DEBUG - Cambiar a False en producción
DEBUG = False  # ⚠️ CAMBIAR de True a False

# ALLOWED_HOSTS - Agregar tu dominio de PythonAnywhere
ALLOWED_HOSTS = ['tu-usuario.pythonanywhere.com', 'localhost', '127.0.0.1']
# Reemplaza 'tu-usuario' con tu username real de PythonAnywhere

# STATIC_ROOT - Agregar esta línea si no existe
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# DATABASES - Ya está configurado para SQLite, déjalo así
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS - Agregar tu dominio
CORS_ALLOWED_ORIGINS = [
    "https://tu-usuario.pythonanywhere.com",
]
```

**Guardar:** `Ctrl + O`, `Enter`, `Ctrl + X`

---

## Paso 6: Migrar Base de Datos

```bash
# Asegúrate de estar en el directorio del proyecto
cd ~/burritos-to-go-api

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario (opcional, si no copias la BD local)
python manage.py createsuperuser
```

**Resultado esperado:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions, authtoken
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

---

## Paso 7: Copiar Datos Locales a PythonAnywhere

### Opción A: Subir la base de datos completa (RECOMENDADO)

**En tu máquina local:**

```bash
# Ir al directorio del proyecto
cd "D:\prado\UTH 2025-3\APLICACION WEB\Files\U3\burritos_to_go"

# Hacer backup de la base de datos
copy db.sqlite3 db_backup.sqlite3
```

**Subir a PythonAnywhere:**

1. En PythonAnywhere, ve a **Files**
2. Navega a: `/home/tu-usuario/burritos-to-go-api/`
3. Click en **"Upload a file"**
4. Selecciona tu archivo `db.sqlite3` local
5. Reemplaza el archivo existente

### Opción B: Exportar e importar datos con fixtures

**En tu máquina local:**

```bash
# Exportar datos a JSON
python manage.py dumpdata core --indent 2 > data_backup.json

# Exportar usuarios
python manage.py dumpdata auth.User --indent 2 > users_backup.json
```

**Subir los archivos JSON:**

1. Sube `data_backup.json` y `users_backup.json` a PythonAnywhere (Files)
2. En la consola Bash de PythonAnywhere:

```bash
cd ~/burritos-to-go-api

# Importar usuarios
python manage.py loaddata users_backup.json

# Importar datos
python manage.py loaddata data_backup.json
```

---

## Paso 8: Configurar Archivos Estáticos

```bash
cd ~/burritos-to-go-api

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

**Resultado esperado:**
```
121 static files copied to '/home/tu-usuario/burritos-to-go-api/staticfiles'
```

---

## Paso 9: Configurar Web App

### 9.1 Crear Web App

1. Ve a la pestaña **Web**
2. Click en **"Add a new web app"**
3. Click **"Next"**
4. Selecciona **"Manual configuration"**
5. Selecciona **"Python 3.10"**
6. Click **"Next"**

### 9.2 Configurar Virtual Environment

En la sección **Virtualenv:**

1. Click en el link **"Enter path to a virtualenv"**
2. Ingresa: `/home/tu-usuario/.virtualenvs/burritos_env`
   (Reemplaza `tu-usuario` con tu username)
3. Click en el check ✓

### 9.3 Configurar WSGI File

1. En la sección **Code**, click en el archivo **WSGI configuration file**
2. **Borra todo el contenido**
3. Pega el siguiente código:

```python
import os
import sys

# Agregar el directorio del proyecto al path
path = '/home/TU_USUARIO/burritos-to-go-api'  # ⚠️ CAMBIAR TU_USUARIO
if path not in sys.path:
    sys.path.append(path)

# Configurar Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'

# Importar la aplicación WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**⚠️ IMPORTANTE:** Reemplaza `TU_USUARIO` con tu username real de PythonAnywhere

4. Click **"Save"**

### 9.4 Configurar Archivos Estáticos

En la sección **Static files:**

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/TU_USUARIO/burritos-to-go-api/staticfiles` |
| `/media/` | `/home/TU_USUARIO/burritos-to-go-api/media` |

**⚠️ Reemplaza `TU_USUARIO`**

### 9.5 Reload Web App

1. Scroll arriba
2. Click en el botón verde **"Reload tu-usuario.pythonanywhere.com"**

---

## Paso 10: Verificar Funcionamiento

### 10.1 Probar la Aplicación

Abre en tu navegador:

```
https://tu-usuario.pythonanywhere.com/api/
```

Deberías ver la página de Django REST Framework.

### 10.2 Probar Endpoints

#### Login:
```
POST https://tu-usuario.pythonanywhere.com/api/auth/login/
Body: {"username": "cliente", "password": "cliente123"}
```

#### Menú (público):
```
GET https://tu-usuario.pythonanywhere.com/api/cliente/menu/
```

#### Dashboard Cliente:
```
https://tu-usuario.pythonanywhere.com/api/panel/
```

#### Dashboard Admin:
```
https://tu-usuario.pythonanywhere.com/api/admin-panel/
```

#### Django Admin:
```
https://tu-usuario.pythonanywhere.com/admin/
```

### 10.3 Verificar Base de Datos

```bash
cd ~/burritos-to-go-api
python manage.py shell

# En el shell de Python:
from core.models import Usuario, Producto, Pedido
print(f"Usuarios: {Usuario.objects.count()}")
print(f"Productos: {Producto.objects.count()}")
print(f"Pedidos: {Pedido.objects.count()}")
```

---

## Troubleshooting

### Error: "DisallowedHost"

**Problema:** No agregaste tu dominio a `ALLOWED_HOSTS`

**Solución:**
```python
# En settings.py
ALLOWED_HOSTS = ['tu-usuario.pythonanywhere.com']
```

### Error: "Static files not found"

**Problema:** No ejecutaste `collectstatic`

**Solución:**
```bash
cd ~/burritos-to-go-api
python manage.py collectstatic --noinput
```

Luego configura la ruta en **Web → Static files**

### Error: "ImportError: No module named..."

**Problema:** No instalaste las dependencias o no activaste el virtualenv

**Solución:**
```bash
workon burritos_env
pip install -r requirements.txt
```

### Error: "500 Internal Server Error"

**Problema:** Error en el código o configuración

**Solución:**
1. Ve a **Web → Log files**
2. Abre el **Error log**
3. Lee el error completo
4. En la consola Bash:
```bash
cd ~/burritos-to-go-api
python manage.py check
```

### Los estilos CSS no cargan

**Problema:** Archivos estáticos no configurados correctamente

**Solución:**
1. Verifica que `STATIC_ROOT` esté en `settings.py`
2. Ejecuta `python manage.py collectstatic`
3. Configura la ruta en **Web → Static files**
4. Click en **Reload**

### Base de datos vacía

**Problema:** No copiaste la base de datos local

**Solución:**
- Usa la **Opción A** o **Opción B** del **Paso 7**

---

## URLs Finales del Proyecto

Una vez desplegado, tu aplicación estará disponible en:

- **API REST:** `https://tu-usuario.pythonanywhere.com/api/`
- **Dashboard Cliente:** `https://tu-usuario.pythonanywhere.com/api/panel/`
- **Dashboard Admin:** `https://tu-usuario.pythonanywhere.com/api/admin-panel/`
- **Django Admin:** `https://tu-usuario.pythonanywhere.com/admin/`

---

## Actualizar el Código

Cuando hagas cambios en GitHub:

```bash
cd ~/burritos-to-go-api
git pull origin main
python manage.py migrate  # Si hay migraciones nuevas
python manage.py collectstatic --noinput  # Si cambiaste CSS/JS
```

Luego en **Web**, click en **Reload**

---

## Comandos Útiles

```bash
# Ver logs en tiempo real
tail -f /var/log/tu-usuario.pythonanywhere.com.error.log

# Reiniciar la aplicación
# (desde Web → Reload button)

# Ver procesos
ps aux | grep python

# Limpiar base de datos y empezar de nuevo
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## Checklist Final

- [ ] Repositorio clonado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] `settings.py` configurado (DEBUG, ALLOWED_HOSTS, STATIC_ROOT)
- [ ] Migraciones ejecutadas
- [ ] Base de datos copiada/importada
- [ ] Archivos estáticos recolectados
- [ ] Web App creada
- [ ] Virtual environment configurado
- [ ] WSGI file configurado
- [ ] Static files configurados
- [ ] Web App reloaded
- [ ] Endpoints funcionando
- [ ] Dashboards accesibles
- [ ] Usuarios pueden hacer login

---

## Contacto y Soporte

Si tienes problemas, revisa:
1. **Error log** en PythonAnywhere (Web → Log files)
2. **Server log** para ver requests
3. Ejecuta `python manage.py check` en la consola

---

**¡Tu aplicación Burritos To Go ya está en producción!** 🌯🚀

