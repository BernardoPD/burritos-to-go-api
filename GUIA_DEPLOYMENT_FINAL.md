# 🌯 Guía de Deployment en PythonAnywhere - Burritos To Go

## 📋 Requisitos Previos
- Cuenta en [PythonAnywhere](https://www.pythonanywhere.com/) (gratuita o de pago)
- Git instalado localmente
- Acceso a tu repositorio

---

## 🚀 Pasos para Desplegar

### **PASO 1: Preparar tu Código Localmente**

1. **Asegúrate de que tu proyecto esté actualizado:**
```bash
cd "D:\PRADO\UTH 2025-3\APLICACION WEB\Files\U3\burritos_to_go"
git status
```

2. **Sube tu código a GitHub (si aún no lo has hecho):**
```bash
git add .
git commit -m "Preparando proyecto para PythonAnywhere"
git push origin main
```

---

### **PASO 2: Configurar en PythonAnywhere**

#### 2.1 - Crear cuenta y acceder
1. Ve a [www.pythonanywhere.com](https://www.pythonanywhere.com/)
2. Regístrate o inicia sesión
3. Ve al **Dashboard**

#### 2.2 - Clonar el repositorio
1. Abre una **Bash console** (en el Dashboard > Consoles > Bash)
2. Clona tu repositorio:
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git burritos_to_go
cd burritos_to_go
```

#### 2.3 - Crear entorno virtual e instalar dependencias
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### **PASO 3: Configurar la Base de Datos MySQL**

#### 3.1 - Crear base de datos
1. Ve a la pestaña **"Databases"** en PythonAnywhere
2. En "MySQL", establece tu contraseña de MySQL
3. Crea una nueva base de datos llamada: `TU_USUARIO$burritos_db`

#### 3.2 - Anotar credenciales
```
Host: TU_USUARIO.mysql.pythonanywhere-services.com
Database: TU_USUARIO$burritos_db
User: TU_USUARIO
Password: [la contraseña que estableciste]
```

#### 3.3 - Actualizar settings.py
Edita `burritos_project/settings.py` con tus credenciales:

```python
# En settings.py, actualizar la configuración de DATABASES:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TU_USUARIO$burritos_db',
        'USER': 'TU_USUARIO',
        'PASSWORD': 'tu_password_mysql',
        'HOST': 'TU_USUARIO.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

# También actualizar:
DEBUG = False
ALLOWED_HOSTS = ['TU_USUARIO.pythonanywhere.com', 'localhost', '127.0.0.1']
```

---

### **PASO 4: Migrar Base de Datos**

Desde la consola Bash en PythonAnywhere:
```bash
cd ~/burritos_to_go
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu usuario administrador.

---

### **PASO 5: Configurar la Aplicación Web**

#### 5.1 - Crear Web App
1. Ve a la pestaña **"Web"**
2. Click en **"Add a new web app"**
3. Selecciona **Python 3.10**
4. Selecciona **"Manual configuration"** (NO Django)

#### 5.2 - Configurar WSGI
1. En la sección **"Code"**, click en el enlace del archivo WSGI
2. **REEMPLAZA TODO** el contenido con esto:

```python
import os
import sys

# CAMBIAR 'TU_USUARIO' por tu nombre de usuario real
path = '/home/TU_USUARIO/burritos_to_go'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

3. **Guarda el archivo**

#### 5.3 - Configurar Virtual Environment
1. En la pestaña "Web", busca **"Virtualenv"**
2. Ingresa la ruta: `/home/TU_USUARIO/burritos_to_go/venv`

#### 5.4 - Configurar Static Files
En la sección **"Static files"**, añade:

| URL | Directory |
|-----|-----------|
| /static/ | /home/TU_USUARIO/burritos_to_go/static |

Luego en la consola:
```bash
cd ~/burritos_to_go
source venv/bin/activate
python manage.py collectstatic --noinput
```

---

### **PASO 6: Recargar la Aplicación**

1. En la pestaña **"Web"**, click en el botón verde **"Reload"**
2. Visita tu sitio: `https://TU_USUARIO.pythonanywhere.com`

---

## 🧪 Verificar el Despliegue

### Probar los Endpoints

#### 1. Panel de Administración
```
https://TU_USUARIO.pythonanywhere.com/admin/
```

#### 2. API Principal
```
https://TU_USUARIO.pythonanywhere.com/api/
```

#### 3. Endpoints de Clientes
```bash
# Registro
curl -X POST https://TU_USUARIO.pythonanywhere.com/api/clientes/registro/ \
  -H "Content-Type: application/json" \
  -d '{"username":"cliente1","password":"pass123","email":"cliente@test.com","telefono":"1234567890"}'

# Login
curl -X POST https://TU_USUARIO.pythonanywhere.com/api/clientes/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"cliente1","password":"pass123"}'

# Ver menú
curl https://TU_USUARIO.pythonanywhere.com/api/clientes/menu/
```

---

## 🔧 Solución de Problemas Comunes

### Error 500: Internal Server Error
1. Ve a **Web** > **Error log** para ver los detalles
2. Verifica que las credenciales de la base de datos sean correctas
3. Asegúrate de que el WSGI esté bien configurado

### Error: No module named 'mysqlclient'
```bash
cd ~/burritos_to_go
source venv/bin/activate
pip install mysqlclient
```

### Error de conexión a MySQL
- Verifica que el host sea: `TU_USUARIO.mysql.pythonanywhere-services.com`
- Verifica que el nombre de la BD sea: `TU_USUARIO$burritos_db`
- Verifica tu contraseña en la pestaña "Databases"

### Static files no cargan
```bash
cd ~/burritos_to_go
source venv/bin/activate
python manage.py collectstatic --noinput
# Luego reload en la pestaña Web
```

---

## 📝 Actualizar tu Aplicación

Cuando hagas cambios en tu código:

```bash
# En PythonAnywhere Bash console
cd ~/burritos_to_go
source venv/bin/activate
git pull origin main
pip install -r requirements.txt  # si hay nuevas dependencias
python manage.py migrate  # si hay nuevas migraciones
python manage.py collectstatic --noinput  # si hay cambios en archivos estáticos
# Luego ir a la pestaña Web y click en Reload
```

---

## 📊 Configuración de Seguridad Adicional

Para producción, considera:

1. **Cambiar SECRET_KEY** en `settings.py`
2. **Configurar HTTPS** (PythonAnywhere lo incluye gratis)
3. **Configurar CORS** si tienes un frontend separado
4. **Backups regulares** de tu base de datos

---

## 🎯 URLs del Sistema Desplegado

Una vez desplegado, tendrás acceso a:

- **Panel Admin**: `https://TU_USUARIO.pythonanywhere.com/admin/`
- **API Root**: `https://TU_USUARIO.pythonanywhere.com/api/`
- **Panel Empleado**: `https://TU_USUARIO.pythonanywhere.com/api/panel/`
- **Endpoints Cliente**: `https://TU_USUARIO.pythonanywhere.com/api/clientes/`

---

## ✅ Checklist Final

- [ ] Código subido a GitHub
- [ ] Cuenta de PythonAnywhere creada
- [ ] Repositorio clonado en PythonAnywhere
- [ ] Virtual environment creado
- [ ] Dependencias instaladas
- [ ] Base de datos MySQL creada
- [ ] Settings.py actualizado con credenciales correctas
- [ ] Migraciones ejecutadas
- [ ] Superuser creado
- [ ] Web app configurada
- [ ] WSGI configurado correctamente
- [ ] Virtual environment vinculado
- [ ] Static files configurados
- [ ] Aplicación recargada
- [ ] Sitio funcionando correctamente

---

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs en la pestaña "Web" > "Error log"
2. Revisa los logs en la pestaña "Web" > "Server log"
3. Consulta la documentación de PythonAnywhere: https://help.pythonanywhere.com/

---

¡Tu API de Burritos To Go estará lista para usar! 🎉
