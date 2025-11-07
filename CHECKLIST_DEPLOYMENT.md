# ✅ Checklist de Deployment - PythonAnywhere

## 📋 Antes de Empezar

- [ ] Tienes cuenta en PythonAnywhere
- [ ] Conoces tu nombre de usuario de PythonAnywhere
- [ ] Tu código está en GitHub (opcional pero recomendado)
- [ ] Has probado el proyecto localmente

---

## 🔧 Configuración Inicial

### En PythonAnywhere:

- [ ] Has abierto una consola Bash
- [ ] Has clonado o subido tu proyecto
- [ ] El proyecto está en: `/home/TU_USUARIO/burritos_to_go`

### Virtual Environment:

- [ ] Has creado el virtual environment: `python3.10 -m venv venv`
- [ ] Has activado el venv: `source venv/bin/activate`
- [ ] Has actualizado pip: `pip install --upgrade pip`
- [ ] Has instalado dependencias: `pip install -r requirements.txt`
- [ ] Todas las dependencias se instalaron sin errores

---

## 🗄️ Base de Datos MySQL

- [ ] Has ido a la pestaña "Databases"
- [ ] Has creado una contraseña MySQL
- [ ] Has anotado la contraseña en un lugar seguro
- [ ] Has creado la base de datos: `TU_USUARIO$burritos_db`
- [ ] Has anotado las credenciales:
  ```
  Host: TU_USUARIO.mysql.pythonanywhere-services.com
  DB Name: TU_USUARIO$burritos_db
  User: TU_USUARIO
  Password: [tu contraseña]
  ```

---

## ⚙️ Configuración de settings.py

- [ ] Has editado `burritos_project/settings.py`
- [ ] Has actualizado `DATABASES` con:
  - [ ] `NAME`: `TU_USUARIO$burritos_db`
  - [ ] `USER`: `TU_USUARIO`
  - [ ] `PASSWORD`: tu contraseña MySQL
  - [ ] `HOST`: `TU_USUARIO.mysql.pythonanywhere-services.com`
- [ ] Has cambiado `DEBUG = False`
- [ ] Has actualizado `ALLOWED_HOSTS = ['TU_USUARIO.pythonanywhere.com']`
- [ ] Has guardado los cambios

---

## 🔄 Migraciones

- [ ] Has ejecutado: `python manage.py makemigrations`
- [ ] Has ejecutado: `python manage.py migrate`
- [ ] No hubo errores en las migraciones
- [ ] Has creado superuser: `python manage.py createsuperuser`
- [ ] Has anotado las credenciales del superuser

---

## 🌐 Configuración Web App

### Crear Web App:

- [ ] Has ido a la pestaña "Web"
- [ ] Has clickeado "Add a new web app"
- [ ] Has seleccionado Python 3.10
- [ ] Has seleccionado "Manual configuration"

### Configurar WSGI:

- [ ] Has clickeado en el archivo WSGI
- [ ] Has borrado TODO el contenido anterior
- [ ] Has pegado el código del archivo `pythonanywhere_wsgi.py`
- [ ] Has cambiado 'TU_USUARIO' por tu usuario real
- [ ] Has guardado el archivo (Ctrl+S o Save)

### Virtual Environment:

- [ ] Has ido a la sección "Virtualenv"
- [ ] Has ingresado: `/home/TU_USUARIO/burritos_to_go/venv`
- [ ] El path se ha guardado correctamente

### Static Files:

- [ ] Has añadido en "Static files":
  - URL: `/static/`
  - Directory: `/home/TU_USUARIO/burritos_to_go/static`
- [ ] Has ejecutado: `python manage.py collectstatic --noinput`
- [ ] Los archivos estáticos se copiaron correctamente

---

## 🚀 Lanzamiento

- [ ] Has clickeado el botón verde "Reload" en la pestaña Web
- [ ] Has esperado a que termine de recargar
- [ ] Has visitado: `https://TU_USUARIO.pythonanywhere.com/`
- [ ] El sitio carga sin error 500

---

## ✅ Verificación

### URLs Funcionando:

- [ ] **Homepage**: `https://TU_USUARIO.pythonanywhere.com/`
- [ ] **API Root**: `https://TU_USUARIO.pythonanywhere.com/api/`
- [ ] **Admin**: `https://TU_USUARIO.pythonanywhere.com/admin/`
- [ ] **Panel Empleado**: `https://TU_USUARIO.pythonanywhere.com/api/panel/`

### Endpoints de Cliente:

- [ ] Registro: `POST /api/clientes/registro/`
- [ ] Login: `POST /api/clientes/login/`
- [ ] Menú: `GET /api/clientes/menu/`
- [ ] Pedidos: `GET /api/clientes/pedidos/`
- [ ] Crear Pedido: `POST /api/clientes/pedidos/`

### Pruebas Básicas:

- [ ] Puedes iniciar sesión en el admin
- [ ] Puedes ver el menú desde la API
- [ ] Puedes registrar un cliente nuevo
- [ ] Puedes hacer login con el cliente
- [ ] Puedes crear un pedido

---

## 🎯 Datos de Acceso a Guardar

```
===========================================
DATOS DE PYTHONANYWHERE
===========================================

URL del Sitio:
https://_____________________.pythonanywhere.com

Usuario PythonAnywhere:
_____________________

Contraseña PythonAnywhere:
_____________________

===========================================
BASE DE DATOS MYSQL
===========================================

Host: _____________________.mysql.pythonanywhere-services.com
Database: _____________________$burritos_db
User: _____________________
Password: _____________________

===========================================
ADMIN DJANGO
===========================================

URL: https://_____________________.pythonanywhere.com/admin/
Username: _____________________
Password: _____________________

===========================================
```

---

## 🔍 Si Algo No Funciona

### Ver Logs:

- [ ] Has revisado el "Error log"
- [ ] Has revisado el "Server log"
- [ ] Has identificado el error específico

### Errores Comunes:

**Error 500 - Internal Server Error:**
- [ ] Verifica settings.py (credenciales DB)
- [ ] Verifica WSGI (ruta del proyecto)
- [ ] Revisa Error log para detalles

**No module named 'X':**
- [ ] Reactiva venv: `source venv/bin/activate`
- [ ] Reinstala: `pip install -r requirements.txt`
- [ ] Reload la web app

**Database connection error:**
- [ ] Verifica nombre de DB: `TU_USUARIO$burritos_db`
- [ ] Verifica host: `TU_USUARIO.mysql.pythonanywhere-services.com`
- [ ] Verifica password en Databases tab

**Static files no cargan:**
- [ ] Ejecuta: `python manage.py collectstatic --noinput`
- [ ] Verifica path en Static files
- [ ] Reload la web app

---

## 🎉 ¡Completado!

Si has marcado todas las casillas, tu API está:
- ✅ Desplegada
- ✅ Funcionando
- ✅ Accesible desde internet
- ✅ Lista para usar con tu app móvil

---

## 📱 Siguiente Paso

Usa estas URLs en tu aplicación Flutter/React Native:

```dart
// En tu app móvil
const String BASE_URL = "https://TU_USUARIO.pythonanywhere.com";
const String API_URL = "$BASE_URL/api/clientes/";
```

---

## 🔄 Para Actualizar en el Futuro

Cuando hagas cambios:

```bash
cd ~/burritos_to_go
source venv/bin/activate
git pull origin main  # si usas GitHub
python manage.py migrate  # si hay nuevas migraciones
python manage.py collectstatic --noinput  # si cambias archivos estáticos
# Luego Reload en la pestaña Web
```

---

**Fecha de deployment**: _______________

**Notas adicionales**:
```
_________________________________
_________________________________
_________________________________
```
