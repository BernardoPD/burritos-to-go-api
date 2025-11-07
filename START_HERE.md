# 🚀 START HERE - Deploy a PythonAnywhere

## 🎯 TODO LO QUE NECESITAS EN 1 PÁGINA

---

## PASO 1: Preparar Localmente (2 minutos)

```bash
# En tu terminal local:
cd "D:\PRADO\UTH 2025-3\APLICACION WEB\Files\U3\burritos_to_go"
git add .
git commit -m "Deploy to PythonAnywhere"
git push origin main
```

---

## PASO 2: PythonAnywhere Setup (5 minutos)

### A) Crear cuenta
👉 https://www.pythonanywhere.com/registration/register/beginner/

### B) Abrir Bash Console y ejecutar:
```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git burritos_to_go
cd burritos_to_go
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## PASO 3: MySQL (3 minutos)

### A) En pestaña "Databases":
1. Crear password MySQL
2. Crear database: `TU_USUARIO$burritos_db`

### B) Editar `burritos_project/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TU_USUARIO$burritos_db',
        'USER': 'TU_USUARIO',
        'PASSWORD': 'tu_password',
        'HOST': 'TU_USUARIO.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

DEBUG = False
ALLOWED_HOSTS = ['TU_USUARIO.pythonanywhere.com']
```

### C) Migrar:
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## PASO 4: Web App (3 minutos)

### A) Pestaña "Web" → Add new web app:
- Python 3.10
- Manual configuration

### B) WSGI File (reemplazar TODO):
```python
import os
import sys

path = '/home/TU_USUARIO/burritos_to_go'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### C) Virtualenv:
```
/home/TU_USUARIO/burritos_to_go/venv
```

### D) Static files:
```bash
python manage.py collectstatic --noinput
```

En la web app, añadir:
- URL: `/static/`
- Directory: `/home/TU_USUARIO/burritos_to_go/static`

---

## PASO 5: Launch (1 minuto)

1. Click "Reload" (botón verde)
2. Visitar: `https://TU_USUARIO.pythonanywhere.com`

---

## ✅ Verificar

- [ ] `https://TU_USUARIO.pythonanywhere.com/` → Funciona
- [ ] `https://TU_USUARIO.pythonanywhere.com/admin/` → Login funciona
- [ ] `https://TU_USUARIO.pythonanywhere.com/api/` → API responde

---

## 🆘 Error 500?

Ver logs: Web → Error log

**Problemas comunes:**
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Verificar migraciones
python manage.py migrate

# Recolectar static
python manage.py collectstatic --noinput
```

---

## 📱 URLs para tu App

```
Base URL: https://TU_USUARIO.pythonanywhere.com

Endpoints:
- Registro: POST /api/clientes/registro/
- Login: POST /api/clientes/login/
- Menú: GET /api/clientes/menu/
- Pedidos: GET /api/clientes/pedidos/
- Crear Pedido: POST /api/clientes/pedidos/
```

---

## 📚 Más Ayuda?

- **Guía completa**: `GUIA_DEPLOYMENT_FINAL.md`
- **Paso a paso**: `PASO_A_PASO_PYTHONANYWHERE.md`
- **Checklist**: `CHECKLIST_DEPLOYMENT.md`

---

**¡15 minutos y estás en producción!** 🎉
