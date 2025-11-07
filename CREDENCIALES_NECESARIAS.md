# 🔐 CREDENCIALES Y DATOS NECESARIOS PARA DEPLOYMENT

## ✅ PASO 1: GitHub (YA COMPLETADO)

**✓ Repositorio GitHub:**
```
https://github.com/BernardoPD/burritos-to-go-api.git
```

**✓ Estado:** Código subido exitosamente
**✓ Commit:** 77c620e - "Preparado para PythonAnywhere deployment"

---

## 📋 PASO 2: Crear Cuenta en PythonAnywhere

### 🌐 Registrarse:
👉 **URL:** https://www.pythonanywhere.com/registration/register/beginner/

### ⚠️ IMPORTANTE - Anota estos datos:

```
┌─────────────────────────────────────────┐
│   DATOS DE PYTHONANYWHERE               │
├─────────────────────────────────────────┤
│                                         │
│ Usuario: _________________________     │
│                                         │
│ Email: ___________________________     │
│                                         │
│ Password: _________________________    │
│                                         │
└─────────────────────────────────────────┘
```

**Ejemplo:**
- Usuario: `juanperez`
- Tu sitio será: `https://juanperez.pythonanywhere.com`

---

## 🗄️ PASO 3: Credenciales MySQL (Crear en PythonAnywhere)

### Dónde crearlas:
1. Inicia sesión en PythonAnywhere
2. Ve a la pestaña **"Databases"**
3. En la sección **"MySQL"**, crea una contraseña

### ⚠️ ANOTA ESTAS CREDENCIALES:

```
┌──────────────────────────────────────────────────┐
│   CREDENCIALES MYSQL                             │
├──────────────────────────────────────────────────┤
│                                                  │
│ Host:                                            │
│   _______________.mysql.pythonanywhere-services.com│
│   (usa tu usuario de PythonAnywhere arriba)     │
│                                                  │
│ Database Name:                                   │
│   _______________$burritos_db                    │
│   (usa tu usuario + $burritos_db)                │
│                                                  │
│ User:                                            │
│   _______________ (mismo que tu usuario PA)      │
│                                                  │
│ Password:                                        │
│   _____________________________                  │
│   (la que acabas de crear en Databases)          │
│                                                  │
│ Port: 3306                                       │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Ejemplo para usuario `juanperez`:**
```
Host: juanperez.mysql.pythonanywhere-services.com
Database: juanperez$burritos_db
User: juanperez
Password: MiPassw0rd123!
Port: 3306
```

---

## 👤 PASO 4: Crear Superusuario Django

Después de migrar la base de datos, crearás un superusuario para el admin de Django.

### ⚠️ ANOTA ESTAS CREDENCIALES:

```
┌─────────────────────────────────────────┐
│   SUPERUSUARIO DJANGO ADMIN             │
├─────────────────────────────────────────┤
│                                         │
│ Username: _________________________    │
│                                         │
│ Email: ___________________________     │
│                                         │
│ Password: _________________________    │
│                                         │
└─────────────────────────────────────────┘
```

**Recomendación:**
- Username: `admin`
- Email: tu email
- Password: una contraseña segura

---

## 📝 RESUMEN DE COMANDOS EN PYTHONANYWHERE

### 1. Clonar el repositorio:
```bash
git clone https://github.com/BernardoPD/burritos-to-go-api.git burritos_to_go
cd burritos_to_go
```

### 2. Crear entorno virtual:
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Editar settings.py con tus credenciales:
```bash
# Usa el editor web de PythonAnywhere o:
nano burritos_project/settings.py
```

**Cambiar estas líneas:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TU_USUARIO$burritos_db',      # ← Cambiar
        'USER': 'TU_USUARIO',                   # ← Cambiar
        'PASSWORD': 'tu_password_mysql',        # ← Cambiar
        'HOST': 'TU_USUARIO.mysql.pythonanywhere-services.com',  # ← Cambiar
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

DEBUG = False
ALLOWED_HOSTS = ['TU_USUARIO.pythonanywhere.com']  # ← Cambiar
```

### 4. Migrar base de datos:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Configurar Web App:
- Ve a pestaña **"Web"**
- Add new web app → Python 3.10 → Manual configuration

### 6. Configurar WSGI:
```python
import os
import sys

# ⚠️ Cambiar TU_USUARIO por tu usuario real
path = '/home/TU_USUARIO/burritos_to_go'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 7. Configurar Virtualenv:
```
/home/TU_USUARIO/burritos_to_go/venv
```

### 8. Collectstatic:
```bash
python manage.py collectstatic --noinput
```

**En Static files (pestaña Web):**
- URL: `/static/`
- Directory: `/home/TU_USUARIO/burritos_to_go/static`

### 9. Reload:
Click el botón verde **"Reload"** en la pestaña Web

---

## 🎯 URLs FINALES

Una vez completado, tu API estará disponible en:

```
┌──────────────────────────────────────────────────┐
│   URLs DE TU API DESPLEGADA                      │
├──────────────────────────────────────────────────┤
│                                                  │
│ Homepage:                                        │
│   https://_____________________.pythonanywhere.com│
│                                                  │
│ Admin Panel:                                     │
│   https://_____________________.pythonanywhere.com/admin/│
│                                                  │
│ API Root:                                        │
│   https://_____________________.pythonanywhere.com/api/│
│                                                  │
│ API Clientes:                                    │
│   https://_____________________.pythonanywhere.com/api/clientes/│
│                                                  │
│ Panel Empleado:                                  │
│   https://_____________________.pythonanywhere.com/api/panel/│
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 📋 CHECKLIST RÁPIDO

- [ ] Creé cuenta en PythonAnywhere
- [ ] Anoté mi usuario de PythonAnywhere
- [ ] Cloné el repositorio desde GitHub
- [ ] Creé el virtual environment
- [ ] Instalé las dependencias
- [ ] Creé contraseña MySQL
- [ ] Creé base de datos `MI_USUARIO$burritos_db`
- [ ] Anoté todas las credenciales MySQL
- [ ] Edité settings.py con mis credenciales
- [ ] Ejecuté las migraciones
- [ ] Creé el superusuario Django
- [ ] Anoté credenciales del superusuario
- [ ] Configuré la Web App
- [ ] Configuré el archivo WSGI
- [ ] Configuré el Virtualenv
- [ ] Ejecuté collectstatic
- [ ] Configuré Static files
- [ ] Hice Reload de la web app
- [ ] Probé que el sitio funcione

---

## 🔒 SEGURIDAD

### ⚠️ IMPORTANTE:
- **NO** compartas estas credenciales públicamente
- **NO** las subas a GitHub
- Guárdalas en un lugar seguro (gestor de contraseñas)
- Usa contraseñas diferentes para cada servicio

---

## 📱 PRÓXIMOS PASOS

Una vez desplegado, usa estas URLs en tu aplicación móvil:

```dart
// Flutter
class ApiConfig {
  static const String baseUrl = 'https://TU_USUARIO.pythonanywhere.com';
  static const String apiUrl = '$baseUrl/api/clientes/';
}
```

```javascript
// React Native
const API_CONFIG = {
  baseUrl: 'https://TU_USUARIO.pythonanywhere.com',
  apiUrl: '/api/clientes/'
};
```

---

## 🆘 ¿PROBLEMAS?

### Ver logs:
- Pestaña Web → **Error log**
- Pestaña Web → **Server log**

### Comandos útiles:
```bash
# Verificar que todo esté instalado
pip list

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Ver migraciones
python manage.py showmigrations

# Probar conexión a BD
python manage.py dbshell
```

---

## 📞 SOPORTE

- **Guía completa**: `GUIA_DEPLOYMENT_FINAL.md`
- **Paso a paso**: `PASO_A_PASO_PYTHONANYWHERE.md`
- **Checklist**: `CHECKLIST_DEPLOYMENT.md`
- **Inicio rápido**: `START_HERE.md`

---

**¡Todo listo para empezar el deployment!** 🚀

_Fecha: 2025-11-07_
