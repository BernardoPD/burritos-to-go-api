# 🌯 Burritos To Go - API REST

![Django](https://img.shields.io/badge/Django-5.2-green)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.15-blue)
![Python](https://img.shields.io/badge/Python-3.11+-yellow)
![Status](https://img.shields.io/badge/Status-Production-success)

Sistema de gestión de pedidos para restaurante de comida rápida con API REST completa para integración con frontend Flutter.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Documentación API](#documentación-api)
- [Usuarios de Prueba](#usuarios-de-prueba)
- [Endpoints Principales](#endpoints-principales)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Dashboards Web](#dashboards-web)
- [Licencia](#licencia)

---

## ✨ Características

### Para Clientes
- ✅ Registro y autenticación con token
- ✅ Consultar menú de productos por categoría
- ✅ Crear pedidos con validación de saldo
- ✅ Ver historial de pedidos (actuales y pasados)
- ✅ Recargar saldo de cuenta
- ✅ Consultar saldo disponible
- ✅ Dashboard web personalizado

### Para Administradores
- ✅ CRUD completo de usuarios
- ✅ CRUD completo de productos
- ✅ CRUD completo de categorías
- ✅ Gestión de pedidos
- ✅ Actualización de estatus de pedidos
- ✅ Dashboard administrativo con estadísticas
- ✅ Panel de administración de Django

### Funcionalidades del Sistema
- ✅ Descuento automático de saldo al crear pedido
- ✅ Validación de saldo insuficiente
- ✅ Filtrado de pedidos por estatus
- ✅ Autenticación por token (Django REST Framework)
- ✅ API REST completa y documentada
- ✅ Colección de Postman incluida

---

## 🚀 Tecnologías

- **Backend:** Django 5.2
- **API:** Django REST Framework 3.15
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Autenticación:** Token Authentication (DRF)
- **Documentación:** Markdown + Postman Collection
- **Frontend Web:** Django Templates + CSS

---

## 📦 Instalación

### Requisitos Previos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Git

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/burritos_to_go.git
cd burritos_to_go
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos
```bash
python manage.py migrate
```

### 5. Cargar Datos Iniciales
```bash
python manage.py loaddata initial_data.json
```

### 6. Ejecutar Servidor
```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

---

## ⚙️ Configuración

### Variables de Entorno (Opcional)
Crear archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Configuración de Base de Datos

Por defecto usa SQLite. Para PostgreSQL, editar `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'burritos_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 📚 Documentación API

### Archivos de Documentación Incluidos

| Archivo | Descripción |
|---------|-------------|
| `DOCUMENTACION_API_FLUTTER.md` | Documentación completa para Flutter con ejemplos Dart |
| `PAQUETE_FRONTEND_FLUTTER.md` | Quick start guide para frontend |
| `GUIA_ENDPOINTS_CLIENTE.md` | Guía de endpoints para clientes con ejemplos curl |
| `Burritos_API_Collection.postman_collection.json` | Colección de Postman importable |
| `rules.md` | Reglas de negocio y arquitectura técnica |

### URL Base
```
http://localhost:8000/api/
```

### Formato de Datos
- **Request:** JSON (application/json)
- **Response:** JSON (application/json)
- **Autenticación:** Token en header `Authorization: Token <token>`

---

## 👥 Usuarios de Prueba

### Cliente
```
Username: cliente
Password: cliente123
Saldo: $600.00
```

### Administrador
```
Username: admin
Password: admin123
Saldo: $380.00
```

---

## 🔗 Endpoints Principales

### Autenticación

```http
POST /api/auth/register/     # Registrar nuevo usuario
POST /api/auth/login/        # Iniciar sesión
POST /api/auth/logout/       # Cerrar sesión
GET  /api/auth/mi-perfil/    # Ver perfil
```

### Cliente

```http
GET  /api/cliente/menu/               # Ver menú (público)
GET  /api/cliente/mis-pedidos/        # Ver mis pedidos
GET  /api/cliente/mi-saldo/           # Consultar saldo
POST /api/cliente/recargar-saldo/     # Recargar saldo
POST /api/crear_pedido/               # Crear pedido
```

### Administrador

```http
GET    /api/usuarios/          # Listar usuarios
POST   /api/usuarios/          # Crear usuario
PUT    /api/usuarios/{id}/     # Actualizar usuario
DELETE /api/usuarios/{id}/     # Eliminar usuario

GET    /api/productos/         # Listar productos
POST   /api/productos/         # Crear producto
PUT    /api/productos/{id}/    # Actualizar producto
DELETE /api/productos/{id}/    # Eliminar producto

GET    /api/pedidos/           # Listar pedidos
PATCH  /api/pedidos/{id}/      # Actualizar estatus

GET    /api/categorias/        # Listar categorías
POST   /api/categorias/        # Crear categoría
```

---

## 📁 Estructura del Proyecto

```
burritos_to_go/
├── burritos_project/          # Configuración del proyecto Django
│   ├── settings.py            # Configuraciones
│   ├── urls.py                # URLs principales
│   └── wsgi.py                # WSGI para producción
│
├── core/                      # App principal
│   ├── models.py              # Modelos (Usuario, Producto, Pedido, Categoría)
│   ├── views.py               # Vistas API y web
│   ├── serializers.py         # Serializers DRF
│   ├── urls.py                # URLs de la app
│   ├── admin.py               # Configuración del admin
│   ├── templates/core/        # Templates HTML
│   │   ├── base_cliente.html
│   │   ├── cliente_dashboard.html
│   │   ├── admin_dashboard.html
│   │   └── ...
│   └── migrations/            # Migraciones de BD
│
├── venv/                      # Entorno virtual (no en git)
├── db.sqlite3                 # Base de datos (no en git)
├── manage.py                  # CLI de Django
├── requirements.txt           # Dependencias Python
├── .gitignore                 # Archivos ignorados por git
├── README.md                  # Este archivo
│
└── Documentación/
    ├── DOCUMENTACION_API_FLUTTER.md
    ├── PAQUETE_FRONTEND_FLUTTER.md
    ├── GUIA_ENDPOINTS_CLIENTE.md
    ├── Burritos_API_Collection.postman_collection.json
    └── rules.md
```

---

## 🖥️ Dashboards Web

### Panel de Cliente
**URL:** `http://localhost:8000/api/panel/`

**Características:**
- Ver saldo actual
- Estadísticas personales
- Menú de productos
- Crear pedidos
- Ver historial de pedidos
- Recargar saldo

### Panel de Administrador
**URL:** `http://localhost:8000/api/admin-panel/`

**Características:**
- Estadísticas del sistema
- Total de usuarios, productos y pedidos
- Ingresos totales
- Pedidos pendientes
- Últimos usuarios registrados
- Productos por categoría
- Accesos rápidos al admin de Django

### Admin de Django
**URL:** `http://localhost:8000/admin/`

Panel administrativo completo de Django para gestionar todo el sistema.

---

## 🧪 Probar la API

### Con Postman

1. Importar `Burritos_API_Collection.postman_collection.json`
2. Configurar variables:
   - `base_url` = `http://localhost:8000/api`
   - `token` = (se obtiene después del login)
3. Ejecutar el endpoint de Login
4. Copiar el token del response
5. Usar en los demás endpoints

### Con curl

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"cliente","password":"cliente123"}'

# Ver menú
curl http://localhost:8000/api/cliente/menu/

# Crear pedido
curl -X POST http://localhost:8000/api/crear_pedido/ \
  -H "Authorization: Token TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productos":[1,5]}'
```

---

## 🔧 Comandos Útiles

```bash
# Crear superusuario
python manage.py createsuperuser

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Cargar datos iniciales
python manage.py loaddata initial_data.json

# Ejecutar tests
python manage.py test

# Ejecutar servidor
python manage.py runserver

# Shell de Django
python manage.py shell
```

---

## 📊 Modelos de Datos

### Usuario
- `username` - Nombre de usuario
- `email` - Correo electrónico
- `password` - Contraseña (encriptada)
- `rol` - admin o cliente
- `saldo` - Saldo disponible

### Producto
- `nombre` - Nombre del producto
- `descripcion` - Descripción
- `precio` - Precio del producto
- `categoria` - Categoría (FK)
- `activo` - Estado del producto

### Pedido
- `cliente` - Usuario que realizó el pedido (FK)
- `productos` - Productos del pedido (M2M)
- `total` - Total del pedido
- `estatus` - pendiente, en_proceso, completado, cancelado
- `fecha` - Fecha y hora del pedido

### Categoría
- `nombre` - Nombre de la categoría

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abrir Pull Request

---

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 📞 Contacto y Soporte

**Desarrollador:** Backend Team  
**Fecha de Creación:** Octubre 2025  
**Versión:** 1.0.0

Para reportar problemas o solicitar funcionalidades, abrir un issue en GitHub.

---

## 🎯 Roadmap

- [ ] Agregar notificaciones por email
- [ ] Implementar sistema de cupones
- [ ] Agregar imágenes de productos
- [ ] Sistema de calificaciones
- [ ] Historial de transacciones
- [ ] Dashboard con gráficas

---

**¡Gracias por usar Burritos To Go API!** 🌯🚀

