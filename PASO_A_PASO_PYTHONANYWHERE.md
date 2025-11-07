# 🚀 Paso a Paso Rápido - Deployment en PythonAnywhere

## ⚡ 5 Pasos Simples

### **PASO 1: Registrarse en PythonAnywhere**
1. Ve a: https://www.pythonanywhere.com/registration/register/beginner/
2. Crea tu cuenta gratuita
3. Anota tu nombre de usuario (lo necesitarás constantemente)

---

### **PASO 2: Subir tu Código**

#### Opción A - Con GitHub (RECOMENDADO)
```bash
# 1. En tu computadora local, sube el código:
git add .
git commit -m "Deploy to PythonAnywhere"
git push origin main

# 2. En PythonAnywhere, abre una consola Bash y ejecuta:
git clone https://github.com/TU_USUARIO/burritos_to_go.git
cd burritos_to_go
```

#### Opción B - Subir archivos manualmente
1. Ve a "Files" en PythonAnywhere
2. Crea carpeta `burritos_to_go`
3. Sube todos los archivos del proyecto

---

### **PASO 3: Instalar Dependencias**

En la consola Bash de PythonAnywhere:
```bash
cd burritos_to_go
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**⏱️ Esto puede tardar 2-5 minutos**

---

### **PASO 4: Configurar MySQL**

1. Ve a la pestaña **"Databases"** en PythonAnywhere
2. Crea una contraseña MySQL (¡guárdala!)
3. Crea una base de datos con el nombre: `TU_USUARIO$burritos_db`

**Ejemplo:** Si tu usuario es `juan123`, la BD será: `juan123$burritos_db`

4. Edita `burritos_project/settings.py` (puedes usar el editor web):

```python
# Busca la sección DATABASES y cambia:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TU_USUARIO$burritos_db',  # ⚠️ CAMBIAR
        'USER': 'TU_USUARIO',  # ⚠️ CAMBIAR
        'PASSWORD': 'tu_password_mysql',  # ⚠️ CAMBIAR
        'HOST': 'TU_USUARIO.mysql.pythonanywhere-services.com',  # ⚠️ CAMBIAR
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

# Y también cambia:
DEBUG = False
ALLOWED_HOSTS = ['TU_USUARIO.pythonanywhere.com']  # ⚠️ CAMBIAR
```

5. Migra la base de datos:
```bash
cd ~/burritos_to_go
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
```

---

### **PASO 5: Configurar la Web App**

1. Ve a la pestaña **"Web"**
2. Click **"Add a new web app"**
3. Selecciona **Python 3.10**
4. Selecciona **"Manual configuration"**

#### Configurar WSGI:
1. Click en el archivo WSGI (aparece en la sección "Code")
2. **BORRA TODO** y pega esto:

```python
import os
import sys

# ⚠️ CAMBIAR 'TU_USUARIO' por tu usuario real
path = '/home/TU_USUARIO/burritos_to_go'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

3. Guarda el archivo (Ctrl+S)

#### Configurar Virtual Environment:
En la misma pestaña "Web", en la sección "Virtualenv":
```
/home/TU_USUARIO/burritos_to_go/venv
```

#### Configurar Static Files:
En "Static files", añade:
- URL: `/static/`
- Directory: `/home/TU_USUARIO/burritos_to_go/static`

Luego ejecuta en la consola:
```bash
cd ~/burritos_to_go
source venv/bin/activate
python manage.py collectstatic --noinput
```

#### ¡LISTO! Click en el botón verde **"Reload"**

---

## ✅ Verificar que Funciona

Visita tu sitio:
```
https://TU_USUARIO.pythonanywhere.com/
```

Probar admin:
```
https://TU_USUARIO.pythonanywhere.com/admin/
```

Probar API:
```
https://TU_USUARIO.pythonanywhere.com/api/
```

---

## 🔥 Comandos de Emergencia

### Si algo sale mal:
```bash
# Ver logs en tiempo real
tail -f /var/log/TU_USUARIO.pythonanywhere.com.error.log

# Reinstalar dependencias
cd ~/burritos_to_go
source venv/bin/activate
pip install -r requirements.txt --force-reinstall

# Resetear base de datos
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

### Ver logs:
- Ve a la pestaña **"Web"**
- Click en **"Error log"** (arriba a la derecha)
- Click en **"Server log"** (arriba a la derecha)

---

## 📱 URLs de tu API Desplegada

Una vez funcionando:

- **Admin**: `https://TU_USUARIO.pythonanywhere.com/admin/`
- **API Root**: `https://TU_USUARIO.pythonanywhere.com/api/`
- **Registro Cliente**: `https://TU_USUARIO.pythonanywhere.com/api/clientes/registro/`
- **Login Cliente**: `https://TU_USUARIO.pythonanywhere.com/api/clientes/login/`
- **Ver Menú**: `https://TU_USUARIO.pythonanywhere.com/api/clientes/menu/`
- **Hacer Pedido**: `https://TU_USUARIO.pythonanywhere.com/api/clientes/pedidos/`
- **Panel Empleado**: `https://TU_USUARIO.pythonanywhere.com/api/panel/`

---

## 🎯 Requerimientos Mínimos

✅ **Lo que SÍ necesitas:**
- Cuenta PythonAnywhere (gratis)
- Python 3.10 (ya viene en PythonAnywhere)
- Base de datos MySQL (gratis en PythonAnywhere)

❌ **Lo que NO necesitas:**
- Tarjeta de crédito (cuenta gratuita)
- Dominio propio (usas `tuusuario.pythonanywhere.com`)
- Servidor propio
- Instalar Python localmente

---

## ⏱️ Tiempo Estimado

- **Primera vez**: 15-30 minutos
- **Con experiencia**: 5-10 minutos
- **Actualizaciones**: 2-3 minutos

---

## 🆘 ¿Problemas?

1. **Error 500**: Revisa el Error log
2. **Base de datos no conecta**: Verifica credenciales en settings.py
3. **Módulos no encontrados**: Reinstala requirements.txt
4. **Static files no cargan**: Ejecuta collectstatic

---

¡Listo! Tu API estará en línea 🎉
