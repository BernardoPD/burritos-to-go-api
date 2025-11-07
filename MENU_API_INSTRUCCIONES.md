# 📋 Menú de APIs - Burritos To Go

## 🎯 ¿Qué es esto?

He creado un menú profesional e interactivo para acceder a todas las APIs de tu sistema sin necesidad de escribir URLs manualmente.

## 🚀 Cómo Acceder

### Iniciar el Servidor

1. **Activar entorno virtual:**
   ```bash
   cd "D:\PRADO\UTH 2025-3\APLICACION WEB\Files\U3\burritos_to_go"
   .\venv\Scripts\Activate.ps1
   ```

2. **Ejecutar servidor:**
   ```bash
   python manage.py runserver
   ```

3. **Abrir navegador en:**
   - **Página de Inicio:** http://127.0.0.1:8000/
   - **Menú de APIs:** http://127.0.0.1:8000/api/menu/

## 📱 Estructura del Menú

### 🔐 APIs de Administrador
Gestión completa del sistema (requiere autenticación de admin):

#### Gestión de Productos
- ✅ Listar todos los productos
- ✅ Crear nuevo producto
- ✅ Ver detalles de un producto
- ✅ Actualizar producto completo
- ✅ Actualizar producto parcialmente
- ✅ Eliminar producto

#### Gestión de Categorías
- ✅ Listar todas las categorías
- ✅ Crear nueva categoría
- ✅ Ver detalles de una categoría
- ✅ Actualizar categoría
- ✅ Eliminar categoría

#### Gestión de Pedidos
- ✅ Listar todos los pedidos
- ✅ Ver detalles de un pedido
- ✅ Actualizar estado de pedido
- ✅ Cancelar pedido

#### Gestión de Usuarios
- ✅ Listar todos los usuarios
- ✅ Ver detalles de un usuario
- ✅ Actualizar usuario
- ✅ Eliminar usuario

### 👤 APIs de Cliente
Funcionalidades para usuarios finales (requiere autenticación):

#### Consultas
- ✅ Ver menú completo
- ✅ Mis pedidos (historial)
- ✅ Mi saldo actual
- ✅ Mi perfil

#### Acciones
- ✅ Crear nuevo pedido
- ✅ Recargar saldo

### 🔑 APIs de Autenticación
Gestión de sesiones:
- ✅ Registro de usuario
- ✅ Iniciar sesión
- ✅ Cerrar sesión
- ✅ Ver perfil

## 🎨 Características del Menú

### ✨ Interfaz Profesional
- Diseño moderno con gradientes
- Tarjetas interactivas con efectos hover
- Organización por pestañas (Admin, Cliente, Autenticación)
- Responsive (se adapta a móviles y tablets)

### 📊 Información Clara
- **Método HTTP** visible (GET, POST, PUT, PATCH, DELETE)
- **Endpoint completo** en formato código
- **Descripción detallada** de cada API
- **Botón directo** para probar cada API

### 🎯 División por Roles
- **Tab de Admin:** APIs exclusivas para administradores
- **Tab de Cliente:** APIs para usuarios finales
- **Tab de Autenticación:** APIs públicas de login/registro

## 🔧 Uso del Menú

### Probar una API

1. **Selecciona la pestaña** correspondiente (Admin/Cliente/Auth)
2. **Busca la API** que quieres probar
3. **Lee la descripción** y el endpoint
4. **Haz clic en "Probar API"** para abrir el endpoint en una nueva pestaña

### Ejemplo de Uso

**Quiero ver el menú de productos:**
1. Ir a la pestaña "APIs de Cliente"
2. Buscar "Ver Menú"
3. Clic en "Probar API"
4. Se abre: `http://127.0.0.1:8000/api/cliente/menu/`

## 🔐 Autenticación

### Para APIs que requieren autenticación:

1. **Primero inicia sesión:**
   - Ve a: http://127.0.0.1:8000/api-auth/login/
   - O usa el botón en la página de inicio

2. **Luego prueba las APIs protegidas:**
   - Tu sesión se mantiene en el navegador
   - Las APIs de Admin y Cliente funcionarán correctamente

## 📍 URLs Importantes

```
Página de Inicio:       http://127.0.0.1:8000/
Menú de APIs:          http://127.0.0.1:8000/api/menu/
Panel Admin Django:    http://127.0.0.1:8000/admin/
Login REST Framework:  http://127.0.0.1:8000/api-auth/login/
```

## 🎯 Endpoints por Categoría

### Admin APIs (Prefijo: /api/)
```
GET     /api/productos/
POST    /api/productos/
GET     /api/productos/{id}/
PUT     /api/productos/{id}/
PATCH   /api/productos/{id}/
DELETE  /api/productos/{id}/

GET     /api/categorias/
POST    /api/categorias/
GET     /api/categorias/{id}/
PUT     /api/categorias/{id}/
DELETE  /api/categorias/{id}/

GET     /api/pedidos/
GET     /api/pedidos/{id}/
PATCH   /api/pedidos/{id}/
DELETE  /api/pedidos/{id}/

GET     /api/usuarios/
GET     /api/usuarios/{id}/
PUT     /api/usuarios/{id}/
DELETE  /api/usuarios/{id}/
```

### Cliente APIs (Prefijo: /api/cliente/)
```
GET     /api/cliente/menu/
GET     /api/cliente/mis-pedidos/
GET     /api/cliente/mi-saldo/
POST    /api/cliente/recargar-saldo/
POST    /api/crear_pedido/
```

### Auth APIs (Prefijo: /api/auth/)
```
POST    /api/auth/register/
POST    /api/auth/login/
POST    /api/auth/logout/
GET     /api/auth/mi-perfil/
```

## 💡 Ventajas del Menú

✅ **Sin necesidad de recordar URLs**
✅ **Documentación visual de todas las APIs**
✅ **Acceso rápido con un clic**
✅ **Interfaz profesional y moderna**
✅ **División clara por roles**
✅ **Indicadores visuales de métodos HTTP**
✅ **Descripciones detalladas**
✅ **Responsive para cualquier dispositivo**

## 🎨 Paleta de Colores

- **Método GET:** Verde (#4caf50)
- **Método POST:** Azul (#2196f3)
- **Método PUT:** Naranja (#ff9800)
- **Método PATCH:** Morado (#9c27b0)
- **Método DELETE:** Rojo (#f44336)

## 📱 Responsive Design

El menú se adapta automáticamente a:
- 💻 Computadoras de escritorio
- 💻 Laptops
- 📱 Tablets
- 📱 Teléfonos móviles

## 🔄 Actualización del Menú

Si agregas nuevas APIs, simplemente edita:
```
D:\PRADO\UTH 2025-3\APLICACION WEB\Files\U3\burritos_to_go\core\templates\api_menu.html
```

## 🎉 ¡Listo para Usar!

Tu menú está completamente funcional y listo para usar. Solo inicia el servidor y accede a la URL.

---

**Creado por:** GitHub Copilot
**Fecha:** 03/11/2025
**Versión:** 1.0
