# 🚀 Guía de Deployment Manual Simplificada - PythonAnywhere

## ⚡ INSTRUCCIONES RÁPIDAS (30 minutos)

### 📋 INFORMACIÓN DE TU CUENTA
- **Usuario:** `pradodiazbackend`
- **Dominio:** `pradodiazbackend.pythonanywhere.com`
- **Repositorio:** `https://github.com/BernardoPD/burritos-to-go-api.git`

---

## 🎯 PASOS A SEGUIR

### PASO 1: Abrir Consola Bash en PythonAnywhere

1. Ve a: **https://www.pythonanywhere.com**
2. Inicia sesión con tu cuenta: `pradodiazbackend`
3. Click en la pestaña **"Consoles"**
4. Click en **"Bash"**

---

### PASO 2: Clonar el Repositorio

Copia y pega estos comandos **UNO POR UNO** en la consola Bash:

```bash
# Clonar repositorio desde GitHub
git clone https://github.com/BernardoPD/burritos-to-go-api.git

# Entrar al directorio
cd burritos-to-go-api

# Verificar que se clonó correctamente
ls -la
```

**✅ Deberías ver:** `burritos_project/`, `core/`, `manage.py`, `requirements.txt`

---

### PASO 3: Crear Entorno Virtual

```bash
# Crear entorno virtual con Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 burritos_env

# Verificar que esté activo (verás "(burritos_env)" al inicio de la línea)
which python
```

**✅ Deberías ver:** `/home/pradodiazbackend/.virtualenvs/burritos_env/bin/python`

---

### PASO 4: Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list | grep -i django
```

**✅ Deberías ver:** Django, djangorestframework, django-cors-headers

---

### PASO 5: Configurar Settings para Producción

```bash
# Editar settings.py
nano burritos_project/settings.py
```

**Busca y modifica estas líneas:**

1. **DEBUG** (línea ~25):
   ```python
   DEBUG = False  # ⚠️ Cambiar de True a False
   ```

2. **ALLOWED_HOSTS** (línea ~27):
   ```python
   ALLOWED_HOSTS = ['pradodiazbackend.pythonanywhere.com', 'localhost']
   ```

3. **STATIC_ROOT** (agregar después de STATIC_URL, línea ~123):
   ```python
   STATIC_URL = 'static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ⬅️ AGREGAR ESTA LÍNEA
   ```

4. **CORS** (buscar CORS_ALLOWED_ORIGINS, línea ~137):
   ```python
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:8000",
       "http://127.0.0.1:8000",
       "https://pradodiazbackend.pythonanywhere.com",  # ⬅️ AGREGAR ESTA LÍNEA
   ]
   ```

**Guardar:** `Ctrl + O`, `Enter`, `Ctrl + X`

---

### PASO 6: Migrar Base de Datos

```bash
# Ejecutar migraciones
python manage.py migrate

# Deberías ver mensajes de "Applying..."
```

**✅ Deberías ver:** `Applying core.0001_initial... OK`

---

### PASO 7: Recolectar Archivos Estáticos

```bash
# Recolectar todos los archivos CSS, JS, imágenes
python manage.py collectstatic --noinput
```

**✅ Deberías ver:** `121 static files copied to '/home/pradodiazbackend/burritos-to-go-api/staticfiles'`

---

### PASO 8: Crear Web App

1. Ve a la pestaña **"Web"**
2. Click en **"Add a new web app"**
3. Click **"Next"**
4. Selecciona **"Manual configuration"** (NO "Django")
5. Selecciona **"Python 3.10"**
6. Click **"Next"**

---

### PASO 9: Configurar Virtual Environment

En la sección **"Virtualenv"**:

1. Busca: **"Enter path to a virtualenv, if desired"**
2. Ingresa: `/home/pradodiazbackend/.virtualenvs/burritos_env`
3. Click en el ✓ (check azul)

**✅ Deberías ver:** El path guardado en azul

---

### PASO 10: Configurar WSGI File

1. En la sección **"Code"**, busca: **"WSGI configuration file"**
2. Click en el link: `/var/www/pradodiazbackend_pythonanywhere_com_wsgi.py`
3. **Borra TODO el contenido del archivo**
4. Pega exactamente esto:

```python
import os
import sys

# Agregar proyecto al path
path = '/home/pradodiazbackend/burritos-to-go-api'
if path not in sys.path:
    sys.path.append(path)

# Configurar Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'

# Iniciar aplicación
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

5. Click en **"Save"** (botón verde arriba)

---

### PASO 11: Configurar Archivos Estáticos

En la sección **"Static files"**:

Click en **"Enter URL"** y agrega estos dos mapeos:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/pradodiazbackend/burritos-to-go-api/staticfiles` |
| `/media/` | `/home/pradodiazbackend/burritos-to-go-api/media` |

**Cómo agregar:**
1. En "URL", escribe: `/static/`
2. En "Directory", escribe: `/home/pradodiazbackend/burritos-to-go-api/staticfiles`
3. Click en el ✓
4. Repite para `/media/`

---

### PASO 12: Subir Base de Datos Local

**En tu computadora local:**

1. Ve a: `D:\prado\UTH 2025-3\APLICACION WEB\Files\U3\burritos_to_go\`
2. Localiza el archivo: `db.sqlite3`

**En PythonAnywhere:**

1. Ve a la pestaña **"Files"**
2. Navega a: `/home/pradodiazbackend/burritos-to-go-api/`
3. Click en **"Upload a file"**
4. Selecciona tu archivo `db.sqlite3` local
5. Click en **"Upload"**

**✅ Deberías ver:** El archivo `db.sqlite3` en la lista

---

### PASO 13: Reload Web App

1. Ve a la pestaña **"Web"**
2. Scroll arriba
3. Click en el botón verde grande: **"Reload pradodiazbackend.pythonanywhere.com"**
4. Espera 10-15 segundos

---

### PASO 14: ¡PROBAR TU APLICACIÓN!

Abre en tu navegador:

#### ✅ API REST Framework:
```
https://pradodiazbackend.pythonanywhere.com/api/
```

#### ✅ Dashboard Cliente:
```
https://pradodiazbackend.pythonanywhere.com/api/panel/
```
- Usuario: `cliente`
- Contraseña: `cliente123`

#### ✅ Dashboard Admin:
```
https://pradodiazbackend.pythonanywhere.com/api/admin-panel/
```
- Usuario: `admin`
- Contraseña: `admin123`

#### ✅ Django Admin:
```
https://pradodiazbackend.pythonanywhere.com/admin/
```

---

## 🆘 TROUBLESHOOTING

### ❌ Error: "DisallowedHost at /"

**Solución:**
```bash
cd ~/burritos-to-go-api
nano burritos_project/settings.py
# Verifica que ALLOWED_HOSTS tenga: 'pradodiazbackend.pythonanywhere.com'
```
Guarda y **Reload** la web app.

---

### ❌ Error: "Static files not loading (CSS no funciona)"

**Solución:**
```bash
cd ~/burritos-to-go-api
python manage.py collectstatic --noinput
```
Luego verifica que en **Web → Static files** tengas:
- URL: `/static/`
- Directory: `/home/pradodiazbackend/burritos-to-go-api/staticfiles`

**Reload** la web app.

---

### ❌ Error: "500 Internal Server Error"

**Solución:**

1. Ve a: **Web → Log files**
2. Abre el **Error log**
3. Lee el último error

Probablemente sea:
- Falta configurar `STATIC_ROOT` en settings.py
- Error en el WSGI file
- No ejecutaste `collectstatic`

---

### ❌ Base de datos vacía (no hay usuarios/productos)

**Solución:**

Sube tu `db.sqlite3` local siguiendo el **PASO 12**.

O crea datos de prueba:
```bash
cd ~/burritos-to-go-api
python manage.py createsuperuser
```

---

## 📊 CHECKLIST FINAL

Verifica que TODO esté ✅:

- [ ] Repositorio clonado en `/home/pradodiazbackend/burritos-to-go-api/`
- [ ] Entorno virtual creado: `burritos_env`
- [ ] Dependencias instaladas (Django, DRF, CORS)
- [ ] `settings.py` modificado:
  - [ ] `DEBUG = False`
  - [ ] `ALLOWED_HOSTS = ['pradodiazbackend.pythonanywhere.com', ...]`
  - [ ] `STATIC_ROOT` agregado
  - [ ] CORS configurado
- [ ] Migraciones ejecutadas: `python manage.py migrate`
- [ ] Archivos estáticos recolectados: `python manage.py collectstatic`
- [ ] Web App creada (Python 3.10)
- [ ] Virtual environment configurado en Web
- [ ] WSGI file configurado correctamente
- [ ] Static files configurados en Web:
  - [ ] `/static/` → `/home/pradodiazbackend/burritos-to-go-api/staticfiles`
  - [ ] `/media/` → `/home/pradodiazbackend/burritos-to-go-api/media`
- [ ] Base de datos `db.sqlite3` subida
- [ ] Web App recargada (Reload button)
- [ ] Sitio funcionando: `https://pradodiazbackend.pythonanywhere.com/api/`

---

## 🎉 URLs FINALES

Tu aplicación estará disponible en:

- **🌐 API REST:** https://pradodiazbackend.pythonanywhere.com/api/
- **👤 Panel Cliente:** https://pradodiazbackend.pythonanywhere.com/api/panel/
- **⚙️ Panel Admin:** https://pradodiazbackend.pythonanywhere.com/api/admin-panel/
- **🔧 Django Admin:** https://pradodiazbackend.pythonanywhere.com/admin/

---

## 📱 COMPARTIR CON EL EQUIPO DE FLUTTER

Dales esta información:

**Base URL:**
```
https://pradodiazbackend.pythonanywhere.com
```

**Documentación:**
- `DOCUMENTACION_API_FLUTTER.md`
- `PAQUETE_FRONTEND_FLUTTER.md`
- Colección Postman: `Burritos_API_Collection.postman_collection.json`

**Credenciales de prueba:**
- Cliente: `cliente` / `cliente123`
- Admin: `admin` / `admin123`

---

## 🔄 ACTUALIZAR CÓDIGO DESPUÉS

Cuando hagas cambios en GitHub:

```bash
# En la consola Bash de PythonAnywhere
cd ~/burritos-to-go-api
git pull origin main
python manage.py migrate  # Si hay nuevas migraciones
python manage.py collectstatic --noinput  # Si cambiaste CSS/JS
```

Luego en **Web**, click en **"Reload"**.

---

## ⏱️ TIEMPO ESTIMADO

- Pasos 1-7 (Setup inicial): **15 minutos**
- Pasos 8-11 (Configurar Web): **10 minutos**
- Pasos 12-14 (Subir BD y probar): **5 minutos**

**TOTAL: 30 minutos** ⚡

---

## 🎯 ¡LISTO!

Sigue estos pasos **en orden** y en 30 minutos tendrás tu aplicación funcionando en producción.

Si tienes dudas, revisa:
1. **Error log** (Web → Log files)
2. `DEPLOYMENT_PYTHONANYWHERE.md` (guía extendida)
3. Ejecuta: `python manage.py check` en la consola

---

**¡Burritos To Go en producción!** 🌯🚀
