# 🚀 DEPLOYMENT PARA pradodiazbackend.pythonanywhere.com

## ✅ TU INFORMACIÓN

**Usuario PythonAnywhere:** `pradodiazbackend`
**URL de tu API:** `https://pradodiazbackend.pythonanywhere.com`
**Repositorio GitHub:** `https://github.com/BernardoPD/burritos-to-go-api.git`

---

## 📋 CREDENCIALES MYSQL QUE NECESITAS

```
Host: pradodiazbackend.mysql.pythonanywhere-services.com
Database: pradodiazbackend$burritos_db
User: pradodiazbackend
Password: [La que crees en la pestaña Databases]
Port: 3306
```

---

## 🎯 COMANDOS EXACTOS PARA COPIAR/PEGAR

### 1️⃣ En Bash Console de PythonAnywhere:

```bash
# Clonar repositorio
git clone https://github.com/BernardoPD/burritos-to-go-api.git burritos_to_go
cd burritos_to_go

# Crear virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 2️⃣ Editar settings.py

Abre el archivo: `Files` → `burritos_to_go` → `burritos_project` → `settings.py`

**Busca la línea 78-89 y reemplaza con:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pradodiazbackend$burritos_db',
        'USER': 'pradodiazbackend',
        'PASSWORD': 'TU_PASSWORD_MYSQL_AQUI',  # ⚠️ Cambiar por tu password
        'HOST': 'pradodiazbackend.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}
```

**Busca la línea 26 y cambia:**
```python
DEBUG = False
```

**Busca la línea 28 y cambia:**
```python
ALLOWED_HOSTS = ['pradodiazbackend.pythonanywhere.com', 'localhost', '127.0.0.1']
```

**Guarda el archivo (Ctrl+S)**

---

### 3️⃣ Migrar Base de Datos

```bash
cd ~/burritos_to_go
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

**Al crear superuser, anota:**
- Username: ________________
- Email: ___________________
- Password: ________________

---

### 4️⃣ Recolectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

---

### 5️⃣ Configurar Web App

#### A) Crear Web App:
1. Ve a pestaña **"Web"**
2. Click **"Add a new web app"**
3. Selecciona **Python 3.10**
4. Selecciona **"Manual configuration"**

#### B) Configurar WSGI:
En la sección "Code", click en el archivo WSGI.
**BORRA TODO** y pega esto:

```python
import os
import sys

path = '/home/pradodiazbackend/burritos_to_go'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'burritos_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Guarda (Ctrl+S)**

#### C) Configurar Virtualenv:
En la sección "Virtualenv", ingresa:
```
/home/pradodiazbackend/burritos_to_go/venv
```

#### D) Configurar Static Files:
En la sección "Static files", añade:

| URL | Directory |
|-----|-----------|
| /static/ | /home/pradodiazbackend/burritos_to_go/static |

---

### 6️⃣ Reload y Probar

1. Click el botón verde **"Reload"** 
2. Visita: **https://pradodiazbackend.pythonanywhere.com**

---

## 🎯 TUS URLs FINALES

```
Homepage:
https://pradodiazbackend.pythonanywhere.com/

Admin Panel:
https://pradodiazbackend.pythonanywhere.com/admin/

API Root:
https://pradodiazbackend.pythonanywhere.com/api/

API Clientes:
https://pradodiazbackend.pythonanywhere.com/api/clientes/

Endpoints:
• POST /api/clientes/registro/
• POST /api/clientes/login/
• GET  /api/clientes/menu/
• GET  /api/clientes/pedidos/
• POST /api/clientes/pedidos/
• GET  /api/clientes/perfil/
• PUT  /api/clientes/perfil/

Panel Empleado:
https://pradodiazbackend.pythonanywhere.com/api/panel/
```

---

## ✅ CHECKLIST

- [ ] Abrí Bash Console en PythonAnywhere
- [ ] Cloné el repositorio
- [ ] Creé virtual environment
- [ ] Instalé dependencias
- [ ] Fui a pestaña "Databases"
- [ ] Creé contraseña MySQL
- [ ] Creé database: `pradodiazbackend$burritos_db`
- [ ] Anoté password MySQL: _______________
- [ ] Edité settings.py con mis credenciales
- [ ] Ejecuté migraciones
- [ ] Creé superuser
- [ ] Anoté credenciales superuser
- [ ] Ejecuté collectstatic
- [ ] Creé Web App (Python 3.10, Manual)
- [ ] Configuré WSGI
- [ ] Configuré Virtualenv
- [ ] Configuré Static files
- [ ] Hice Reload
- [ ] Probé el sitio - ¡Funciona! ✅

---

## 📱 Para tu App Móvil

```dart
// Flutter
class ApiConfig {
  static const String baseUrl = 'https://pradodiazbackend.pythonanywhere.com';
  static const String apiUrl = '$baseUrl/api/clientes/';
  
  // Endpoints
  static const String registro = '$apiUrl/registro/';
  static const String login = '$apiUrl/login/';
  static const String menu = '$apiUrl/menu/';
  static const String pedidos = '$apiUrl/pedidos/';
  static const String perfil = '$apiUrl/perfil/';
}
```

```javascript
// React Native
const API_CONFIG = {
  baseUrl: 'https://pradodiazbackend.pythonanywhere.com',
  apiUrl: '/api/clientes/',
  
  endpoints: {
    registro: '/api/clientes/registro/',
    login: '/api/clientes/login/',
    menu: '/api/clientes/menu/',
    pedidos: '/api/clientes/pedidos/',
    perfil: '/api/clientes/perfil/'
  }
};
```

---

## 🆘 Si hay Problemas

### Ver logs:
```bash
# En la pestaña Web:
# → Error log (arriba a la derecha)
# → Server log (arriba a la derecha)

# O en Bash:
tail -f /var/log/pradodiazbackend.pythonanywhere.com.error.log
```

### Reinstalar dependencias:
```bash
cd ~/burritos_to_go
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Verificar migraciones:
```bash
python manage.py showmigrations
```

---

## 🔄 Actualizar en el Futuro

```bash
cd ~/burritos_to_go
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# Luego Reload en la pestaña Web
```

---

## 📞 NOTAS IMPORTANTES

1. **Password MySQL**: Lo creas en Databases tab de PythonAnywhere
2. **No compartas** tu password públicamente
3. **Anota** todas las credenciales en lugar seguro
4. **HTTPS**: Ya viene incluido gratis
5. **Base de datos**: El nombre DEBE ser `pradodiazbackend$burritos_db` (con el $)

---

## ✨ LISTO!

Tu API estará disponible en:
**https://pradodiazbackend.pythonanywhere.com**

**Tiempo estimado:** 15-20 minutos

¡Éxito con el deployment! 🚀🌯
