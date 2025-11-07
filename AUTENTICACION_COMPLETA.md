# 🔐 Sistema de Autenticación Completo - Burritos To Go

## ✅ ¿Qué se ha implementado?

Se ha creado un **sistema completo de autenticación** con páginas de login y registro profesionales, totalmente funcionales e integradas con el menú de APIs.

## 📁 Archivos Creados

### Templates HTML
```
core/templates/
├── login.html          - Página de login profesional
├── register.html       - Página de registro
├── api_menu.html       - Menú con estado de autenticación
└── index.html          - Página de inicio actualizada
```

### Scripts
```
crear_usuarios_prueba.py  - Script para crear usuarios de prueba
```

### Modificaciones
```
core/views.py              - Añadidas vistas: login_page_view, register_page_view
burritos_project/urls.py   - Rutas: /login/, /register/
```

## 🚀 URLs del Sistema

### Páginas Principales
```
http://127.0.0.1:8000/              - Página de inicio
http://127.0.0.1:8000/login/        - Login personalizado
http://127.0.0.1:8000/register/     - Registro de usuarios
http://127.0.0.1:8000/api/menu/     - Menú de APIs
```

### APIs de Autenticación
```
POST /api/auth/login/       - API de login (JSON)
POST /api/auth/register/    - API de registro (JSON)
POST /api/auth/logout/      - API de logout
GET  /api/auth/mi-perfil/   - Ver perfil del usuario
```

### Login Django REST Framework
```
http://127.0.0.1:8000/api-auth/login/   - Login DRF (alternativo)
```

## 👥 Usuarios de Prueba

### 🔐 Administrador
```
Username: admin
Password: admin123
Rol: admin
Saldo: $1000.00
Acceso: TODAS las APIs
```

### 👤 Cliente 1
```
Username: cliente1
Password: password123
Rol: cliente
Saldo: $500.00
Acceso: APIs de cliente
```

### 👤 Cliente 2
```
Username: cliente2
Password: password123
Rol: cliente
Saldo: $300.00
Acceso: APIs de cliente
```

## 🎯 Flujo de Autenticación

### Opción 1: Login Personalizado (Recomendado)

```
1. Ir a http://127.0.0.1:8000/login/
   ↓
2. Ingresar credenciales (ver usuarios arriba)
   ↓
3. Clic en "Iniciar Sesión"
   ↓
4. Redirección automática al menú de APIs
   ↓
5. Estado de usuario visible en la esquina superior derecha
```

### Opción 2: Registro de Nuevo Usuario

```
1. Ir a http://127.0.0.1:8000/register/
   ↓
2. Llenar formulario:
   - Nombre y Apellido
   - Usuario
   - Email
   - Contraseña (confirmar)
   ↓
3. Clic en "Registrarse"
   ↓
4. Cuenta creada automáticamente con rol "cliente"
   ↓
5. Redirección al menú de APIs
```

### Opción 3: Login Django REST Framework

```
1. Ir a http://127.0.0.1:8000/api-auth/login/
   ↓
2. Login con interfaz de Django REST Framework
   ↓
3. Navegar manualmente a las APIs
```

## 🎨 Características del Sistema de Login

### ✨ Login Personalizado
- ✅ Diseño profesional con gradientes
- ✅ Validación en tiempo real
- ✅ Mensajes de error claros
- ✅ Loading indicator
- ✅ Credenciales de prueba visibles
- ✅ Link directo a DRF login
- ✅ Responsive design

### ✨ Registro de Usuarios
- ✅ Formulario completo (nombre, apellido, email, etc.)
- ✅ Validación de contraseñas
- ✅ Confirmación de contraseña
- ✅ Rol automático: "cliente"
- ✅ Saldo inicial: $0.00
- ✅ Login automático después del registro

### ✨ Menú de APIs con Autenticación
- ✅ Estado de usuario visible
- ✅ Muestra username, rol y saldo
- ✅ Botón de cerrar sesión
- ✅ Botón de login si no está autenticado
- ✅ Persistencia con localStorage

## 🔐 Sistema de Tokens

### Almacenamiento
```javascript
// Token guardado en localStorage
localStorage.setItem('token', 'abc123...');

// Datos de usuario guardados
localStorage.setItem('usuario', JSON.stringify({
    id: 1,
    username: 'admin',
    rol: 'admin',
    saldo: 1000.00
}));
```

### Uso en APIs
```javascript
// Las APIs protegidas verifican automáticamente la sesión
fetch('/api/productos/', {
    headers: {
        'Authorization': 'Token ' + localStorage.getItem('token')
    }
});
```

## 📊 Respuestas de APIs

### Login Exitoso
```json
{
    "mensaje": "Inicio de sesión exitoso",
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "usuario": {
        "id": 1,
        "username": "admin",
        "email": "admin@burritos.com",
        "rol": "admin",
        "saldo": 1000.0
    }
}
```

### Login Fallido
```json
{
    "error": "Credenciales inválidas"
}
```

### Registro Exitoso
```json
{
    "mensaje": "Usuario registrado exitosamente",
    "token": "8833a08088b51abce8317bd755d4ccaade6ae3a3",
    "usuario": {
        "id": 5,
        "username": "nuevo_usuario",
        "email": "nuevo@example.com",
        "rol": "cliente",
        "saldo": 0.0
    }
}
```

## 🎯 Permisos por Rol

### Admin
```
✅ Ver todos los productos
✅ Crear/Editar/Eliminar productos
✅ Ver todos los pedidos
✅ Actualizar estado de pedidos
✅ Ver todos los usuarios
✅ Gestionar categorías
```

### Cliente
```
✅ Ver menú de productos
✅ Crear pedidos propios
✅ Ver mis pedidos
✅ Consultar mi saldo
✅ Recargar saldo
❌ NO puede ver pedidos de otros
❌ NO puede gestionar productos
```

## 🔄 Cerrar Sesión

### Desde el Menú de APIs
```
1. Estando autenticado, ver esquina superior derecha
   ↓
2. Clic en "Cerrar Sesión"
   ↓
3. Se limpia localStorage
   ↓
4. Se llama a API /api/auth/logout/
   ↓
5. Página se recarga
```

### Mediante API
```javascript
fetch('/api/auth/logout/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    }
});

// Limpiar datos locales
localStorage.removeItem('token');
localStorage.removeItem('usuario');
```

## 🛠️ Crear Más Usuarios

### Opción 1: Script de Python
```bash
# Editar crear_usuarios_prueba.py y ejecutar
python crear_usuarios_prueba.py
```

### Opción 2: Panel de Admin
```
1. Ir a http://127.0.0.1:8000/admin/
2. Login con admin/admin123
3. Usuarios → Añadir usuario
```

### Opción 3: Página de Registro
```
http://127.0.0.1:8000/register/
```

### Opción 4: API de Registro
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo",
    "email": "nuevo@example.com",
    "password": "password123",
    "password2": "password123",
    "first_name": "Nuevo",
    "last_name": "Usuario"
  }'
```

## 🎨 Personalización

### Cambiar Colores
Editar en `login.html` y `register.html`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Cambiar Saldo Inicial
Editar `core/serializers.py`:
```python
user.saldo = Decimal('100.00')  # Cambiar aquí
```

### Modificar Validaciones
Editar `core/serializers.py` en `RegisterSerializer`:
```python
def validate_password(self, value):
    if len(value) < 8:  # Cambiar longitud mínima
        raise serializers.ValidationError("...")
```

## 📱 Responsive Design

Todas las páginas son responsive:
```
Desktop:    > 768px   - Vista completa
Tablet:     768px     - Adaptado
Mobile:     < 768px   - Optimizado para táctil
```

## 🔍 Debugging

### Ver Token en Consola
```javascript
console.log(localStorage.getItem('token'));
console.log(localStorage.getItem('usuario'));
```

### Verificar Autenticación
```javascript
// En la consola del navegador
fetch('/api/auth/mi-perfil/')
  .then(r => r.json())
  .then(data => console.log(data));
```

### Limpiar Sesión
```javascript
localStorage.clear();
location.reload();
```

## ✅ Checklist de Funcionalidades

```
[✓] Página de login profesional
[✓] Página de registro
[✓] API de login
[✓] API de registro
[✓] API de logout
[✓] Usuarios de prueba creados
[✓] Estado de auth en menú
[✓] Persistencia de sesión
[✓] Tokens funcionando
[✓] Validación de permisos
[✓] Responsive design
[✓] Mensajes de error
[✓] Loading states
[✓] Documentación completa
```

## 🎉 ¡Todo Listo!

El sistema de autenticación está completamente funcional:

1. **Inicia el servidor:**
   ```bash
   python manage.py runserver
   ```

2. **Abre el navegador:**
   ```
   http://127.0.0.1:8000/login/
   ```

3. **Usa las credenciales:**
   - Admin: admin / admin123
   - Cliente: cliente1 / password123

4. **Explora el menú de APIs con tu cuenta!**

---

**Fecha:** 03/11/2025
**Versión:** 2.0
**Estado:** ✅ Completamente Funcional
