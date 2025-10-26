# 📱 Documentación API para Flutter - Burritos To Go

**Fecha:** 2025-10-26  
**Versión:** 1.0  
**Backend:** Django REST Framework  
**Base URL:** `http://localhost:8000/api/`

---

## 📋 Tabla de Contenidos

1. [Información General](#información-general)
2. [Autenticación](#autenticación)
3. [Endpoints de Cliente](#endpoints-de-cliente)
4. [Endpoints de Administrador](#endpoints-de-administrador)
5. [Modelos de Datos](#modelos-de-datos)
6. [Códigos de Estado HTTP](#códigos-de-estado-http)
7. [Ejemplos de Uso](#ejemplos-de-uso)
8. [Manejo de Errores](#manejo-de-errores)

---

## 🌐 Información General

### Base URL
```
http://localhost:8000/api/
```

### Formato de Datos
- **Request:** JSON (application/json)
- **Response:** JSON (application/json)

### Autenticación
- **Tipo:** Token Authentication
- **Header:** `Authorization: Token <tu_token>`

### Caracteres Especiales
- **Encoding:** UTF-8
- **Date Format:** ISO 8601 (YYYY-MM-DDTHH:mm:ssZ)

---

## 🔐 Autenticación

### 1. Registrar Usuario (Nuevo Cliente)

**Endpoint:** `POST /api/auth/register/`

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Body:**
```json
{
  "username": "cliente1",
  "email": "cliente1@example.com",
  "password": "password123",
  "password2": "password123",
  "first_name": "Juan",
  "last_name": "Pérez"
}
```

**Response (201):**
```json
{
  "mensaje": "Usuario registrado exitosamente",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "usuario": {
    "id": 3,
    "username": "cliente1",
    "email": "cliente1@example.com",
    "rol": "cliente",
    "saldo": 0.00
  }
}
```

---

### 2. Login (Iniciar Sesión)

**Endpoint:** `POST /api/auth/login/`

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Body:**
```json
{
  "username": "cliente",
  "password": "cliente123"
}
```

**Response (200):**
```json
{
  "mensaje": "Login exitoso",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "usuario": {
    "id": 2,
    "username": "cliente",
    "email": "cliente@example.com",
    "rol": "cliente",
    "saldo": 600.00
  }
}
```

**Response Error (400):**
```json
{
  "error": "Datos inválidos",
  "detalles": {
    "non_field_errors": ["Credenciales inválidas"]
  }
}
```

---

### 3. Logout (Cerrar Sesión)

**Endpoint:** `POST /api/auth/logout/`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Response (200):**
```json
{
  "mensaje": "Sesión cerrada exitosamente"
}
```

---

### 4. Ver Mi Perfil

**Endpoint:** `GET /api/auth/mi-perfil/`

**Headers:**
```json
{
  "Authorization": "Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Response (200):**
```json
{
  "id": 2,
  "username": "cliente",
  "email": "cliente@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "rol": "cliente",
  "saldo": 600.00,
  "date_joined": "2025-10-20T10:30:00Z"
}
```

---

## 👤 Endpoints de Cliente

### 1. Consultar Menú

**Endpoint:** `GET /api/cliente/menu/`

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
*No requiere autenticación*

**Response (200):**
```json
{
  "categorias": [
    {
      "id": 1,
      "nombre": "Burritos",
      "productos": [
        {
          "id": 1,
          "nombre": "Burrito de Carne Asada",
          "descripcion": "Delicioso burrito con carne asada, frijoles, queso y salsa",
          "precio": "80.00",
          "categoria_nombre": "Burritos"
        },
        {
          "id": 2,
          "nombre": "Burrito de Pollo",
          "descripcion": "Burrito de pollo con guacamole",
          "precio": "75.00",
          "categoria_nombre": "Burritos"
        }
      ]
    },
    {
      "id": 2,
      "nombre": "Bebidas",
      "productos": [
        {
          "id": 5,
          "nombre": "Refresco 500ml",
          "descripcion": "Refresco de cola",
          "precio": "20.00",
          "categoria_nombre": "Bebidas"
        }
      ]
    }
  ],
  "total_categorias": 2
}
```

---

### 2. Ver Mis Pedidos

**Endpoint:** `GET /api/cliente/mis-pedidos/`

**Headers:**
```json
{
  "Authorization": "Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Query Params (opcionales):**
- `tipo=actuales` - Solo pedidos pendiente o en_proceso
- `tipo=pasados` - Solo pedidos completado o cancelado
- `estatus=pendiente` - Filtrar por estatus específico

**Ejemplos:**
```
GET /api/cliente/mis-pedidos/
GET /api/cliente/mis-pedidos/?tipo=actuales
GET /api/cliente/mis-pedidos/?tipo=pasados
GET /api/cliente/mis-pedidos/?estatus=pendiente
```

**Response (200):**
```json
{
  "pedidos": [
    {
      "id": 5,
      "cliente": 2,
      "cliente_nombre": "cliente",
      "productos_detalle": [
        {
          "id": 1,
          "nombre": "Burrito de Carne Asada",
          "precio": 80.00
        },
        {
          "id": 5,
          "nombre": "Refresco 500ml",
          "precio": 20.00
        }
      ],
      "total": "100.00",
      "estatus": "pendiente",
      "fecha": "2025-10-26T18:30:00Z"
    }
  ],
  "total": 1,
  "filtros_aplicados": {
    "tipo": "actuales",
    "estatus": null
  }
}
```

---

### 3. Consultar Mi Saldo

**Endpoint:** `GET /api/cliente/mi-saldo/`

**Headers:**
```json
{
  "Authorization": "Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Response (200):**
```json
{
  "saldo": 600.00,
  "usuario": "cliente",
  "email": "cliente@example.com",
  "fecha_consulta": "2025-10-26T18:35:00Z"
}
```

---

### 4. Recargar Saldo

**Endpoint:** `POST /api/cliente/recargar-saldo/`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Body:**
```json
{
  "monto": 100.00
}
```

**Validaciones:**
- Monto mínimo: 0.01
- Monto máximo: 10000.00

**Response (200):**
```json
{
  "mensaje": "Saldo recargado exitosamente",
  "monto_recargado": 100.00,
  "saldo_anterior": 600.00,
  "saldo_actual": 700.00,
  "usuario": "cliente",
  "fecha_recarga": "2025-10-26T18:40:00Z"
}
```

**Response Error (400):**
```json
{
  "error": "Datos inválidos",
  "detalles": {
    "monto": ["El monto debe ser mayor a 0"]
  }
}
```

---

### 5. Crear Pedido

**Endpoint:** `POST /api/crear_pedido/`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Body:**
```json
{
  "productos": [1, 5]
}
```
*Array de IDs de productos*

**Response (200):**
```json
{
  "mensaje": "Pedido creado exitosamente.",
  "pedido_id": 13,
  "total": 100.0,
  "productos": [
    "Burrito de Carne Asada",
    "Refresco 500ml"
  ],
  "fecha": "2025-10-26T18:45:00Z",
  "saldo_restante": 500.0
}
```

**Response Error - Saldo Insuficiente (400):**
```json
{
  "error": "Saldo insuficiente.",
  "saldo_actual": 50.0,
  "total_pedido": 100.0,
  "faltante": 50.0
}
```

**Response Error - Productos Inválidos (400):**
```json
{
  "error": "No se encontraron productos válidos."
}
```

---

## 👨‍💼 Endpoints de Administrador

### 1. Listar Todos los Usuarios

**Endpoint:** `GET /api/usuarios/`

**Headers:**
```json
{
  "Authorization": "Token <admin_token>"
}
```

**Response (200):**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "rol": "admin",
    "saldo": 380.00
  },
  {
    "id": 2,
    "username": "cliente",
    "email": "cliente@example.com",
    "rol": "cliente",
    "saldo": 600.00
  }
]
```

---

### 2. Crear Usuario

**Endpoint:** `POST /api/usuarios/`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Token <admin_token>"
}
```

**Body:**
```json
{
  "username": "nuevo_usuario",
  "email": "nuevo@example.com",
  "password": "password123",
  "rol": "cliente",
  "saldo": 0.00
}
```

**Response (201):**
```json
{
  "id": 4,
  "username": "nuevo_usuario",
  "email": "nuevo@example.com",
  "rol": "cliente",
  "saldo": 0.00
}
```

---

### 3. Listar Todos los Productos

**Endpoint:** `GET /api/productos/`

**Response (200):**
```json
[
  {
    "id": 1,
    "nombre": "Burrito de Carne Asada",
    "descripcion": "Delicioso burrito con carne asada",
    "precio": "80.00",
    "categoria": 1,
    "categoria_nombre": "Burritos",
    "activo": true
  }
]
```

---

### 4. Crear Producto

**Endpoint:** `POST /api/productos/`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Token <admin_token>"
}
```

**Body:**
```json
{
  "nombre": "Burrito Vegetariano",
  "descripcion": "Burrito con verduras frescas",
  "precio": 70.00,
  "categoria": 1,
  "activo": true
}
```

**Response (201):**
```json
{
  "id": 10,
  "nombre": "Burrito Vegetariano",
  "descripcion": "Burrito con verduras frescas",
  "precio": "70.00",
  "categoria": 1,
  "categoria_nombre": "Burritos",
  "activo": true
}
```

---

### 5. Actualizar Producto

**Endpoint:** `PUT /api/productos/{id}/`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Token <admin_token>"
}
```

**Body:**
```json
{
  "nombre": "Burrito Vegetariano Premium",
  "descripcion": "Burrito con verduras orgánicas",
  "precio": 85.00,
  "categoria": 1,
  "activo": true
}
```

**Response (200):**
```json
{
  "id": 10,
  "nombre": "Burrito Vegetariano Premium",
  "descripcion": "Burrito con verduras orgánicas",
  "precio": "85.00",
  "categoria": 1,
  "categoria_nombre": "Burritos",
  "activo": true
}
```

---

### 6. Eliminar Producto

**Endpoint:** `DELETE /api/productos/{id}/`

**Headers:**
```json
{
  "Authorization": "Token <admin_token>"
}
```

**Response (204):**
```
No Content
```

---

### 7. Listar Todos los Pedidos

**Endpoint:** `GET /api/pedidos/`

**Headers:**
```json
{
  "Authorization": "Token <admin_token>"
}
```

**Response (200):**
```json
[
  {
    "id": 1,
    "cliente": 2,
    "productos": [1, 5],
    "total": "100.00",
    "estatus": "pendiente",
    "fecha": "2025-10-26T18:30:00Z"
  }
]
```

---

### 8. Actualizar Estatus de Pedido

**Endpoint:** `PATCH /api/pedidos/{id}/`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Token <admin_token>"
}
```

**Body:**
```json
{
  "estatus": "en_proceso"
}
```

**Valores permitidos para estatus:**
- `pendiente`
- `en_proceso`
- `completado`
- `cancelado`

**Response (200):**
```json
{
  "id": 1,
  "cliente": 2,
  "productos": [1, 5],
  "total": "100.00",
  "estatus": "en_proceso",
  "fecha": "2025-10-26T18:30:00Z"
}
```

---

### 9. Listar Categorías

**Endpoint:** `GET /api/categorias/`

**Response (200):**
```json
[
  {
    "id": 1,
    "nombre": "Burritos"
  },
  {
    "id": 2,
    "nombre": "Bebidas"
  },
  {
    "id": 3,
    "nombre": "Postres"
  }
]
```

---

### 10. Crear Categoría

**Endpoint:** `POST /api/categorias/`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Token <admin_token>"
}
```

**Body:**
```json
{
  "nombre": "Ensaladas"
}
```

**Response (201):**
```json
{
  "id": 4,
  "nombre": "Ensaladas"
}
```

---

## 📦 Modelos de Datos

### Usuario
```json
{
  "id": 1,
  "username": "cliente",
  "email": "cliente@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "rol": "cliente",
  "saldo": 600.00,
  "date_joined": "2025-10-20T10:30:00Z"
}
```

### Producto
```json
{
  "id": 1,
  "nombre": "Burrito de Carne Asada",
  "descripcion": "Delicioso burrito con carne asada",
  "precio": "80.00",
  "categoria": 1,
  "categoria_nombre": "Burritos",
  "activo": true
}
```

### Pedido
```json
{
  "id": 1,
  "cliente": 2,
  "cliente_nombre": "cliente",
  "productos": [1, 5],
  "productos_detalle": [
    {
      "id": 1,
      "nombre": "Burrito de Carne Asada",
      "precio": 80.00
    }
  ],
  "total": "100.00",
  "estatus": "pendiente",
  "fecha": "2025-10-26T18:30:00Z"
}
```

### Categoría
```json
{
  "id": 1,
  "nombre": "Burritos"
}
```

---

## 📝 Códigos de Estado HTTP

| Código | Descripción | Uso |
|--------|-------------|-----|
| 200 | OK | Request exitoso |
| 201 | Created | Recurso creado exitosamente |
| 204 | No Content | Recurso eliminado |
| 400 | Bad Request | Datos inválidos |
| 401 | Unauthorized | No autenticado |
| 403 | Forbidden | Sin permisos |
| 404 | Not Found | Recurso no encontrado |
| 500 | Server Error | Error del servidor |

---

## 💡 Ejemplos de Uso en Flutter

### 1. Configuración Inicial

```dart
class ApiService {
  static const String baseUrl = 'http://localhost:8000/api';
  String? _token;

  void setToken(String token) {
    _token = token;
  }

  Map<String, String> getHeaders({bool includeAuth = true}) {
    Map<String, String> headers = {
      'Content-Type': 'application/json',
    };
    
    if (includeAuth && _token != null) {
      headers['Authorization'] = 'Token $_token';
    }
    
    return headers;
  }
}
```

---

### 2. Login

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>> login(String username, String password) async {
  final url = Uri.parse('${ApiService.baseUrl}/auth/login/');
  
  final response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'username': username,
      'password': password,
    }),
  );
  
  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    // Guardar token
    ApiService().setToken(data['token']);
    return data;
  } else {
    throw Exception('Error en login: ${response.body}');
  }
}
```

---

### 3. Obtener Menú

```dart
Future<List<dynamic>> obtenerMenu() async {
  final url = Uri.parse('${ApiService.baseUrl}/cliente/menu/');
  
  final response = await http.get(url);
  
  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    return data['categorias'];
  } else {
    throw Exception('Error al obtener menú');
  }
}
```

---

### 4. Crear Pedido

```dart
Future<Map<String, dynamic>> crearPedido(List<int> productosIds) async {
  final url = Uri.parse('${ApiService.baseUrl}/crear_pedido/');
  
  final response = await http.post(
    url,
    headers: ApiService().getHeaders(),
    body: jsonEncode({
      'productos': productosIds,
    }),
  );
  
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    final error = jsonDecode(response.body);
    throw Exception(error['error'] ?? 'Error al crear pedido');
  }
}
```

---

### 5. Recargar Saldo

```dart
Future<Map<String, dynamic>> recargarSaldo(double monto) async {
  final url = Uri.parse('${ApiService.baseUrl}/cliente/recargar-saldo/');
  
  final response = await http.post(
    url,
    headers: ApiService().getHeaders(),
    body: jsonEncode({
      'monto': monto,
    }),
  );
  
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Error al recargar saldo');
  }
}
```

---

### 6. Ver Mis Pedidos

```dart
Future<List<dynamic>> verMisPedidos({String? tipo}) async {
  String endpoint = '/cliente/mis-pedidos/';
  if (tipo != null) {
    endpoint += '?tipo=$tipo';
  }
  
  final url = Uri.parse('${ApiService.baseUrl}$endpoint');
  
  final response = await http.get(
    url,
    headers: ApiService().getHeaders(),
  );
  
  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    return data['pedidos'];
  } else {
    throw Exception('Error al obtener pedidos');
  }
}
```

---

## ⚠️ Manejo de Errores

### Estructura de Error Estándar

```json
{
  "error": "Descripción del error",
  "detalles": {
    "campo": ["Mensaje de error específico"]
  }
}
```

### Ejemplo en Flutter

```dart
try {
  final result = await login(username, password);
  // Procesar resultado exitoso
} catch (e) {
  if (e.toString().contains('Credenciales inválidas')) {
    // Mostrar mensaje de credenciales incorrectas
  } else if (e.toString().contains('Saldo insuficiente')) {
    // Mostrar mensaje de saldo insuficiente
  } else {
    // Error genérico
  }
}
```

---

## 🔒 Notas de Seguridad

1. **Almacenamiento de Token:**
   - Usa `SharedPreferences` o `secure_storage` para guardar el token
   - Nunca almacenes el token en variables globales sin encriptación

2. **HTTPS:**
   - En producción, usa HTTPS
   - Cambia `http://localhost:8000` por tu dominio HTTPS

3. **Validación:**
   - Siempre valida los datos antes de enviarlos
   - Maneja todos los casos de error posibles

4. **Timeout:**
   - Configura timeouts apropiados (5-10 segundos)
   - Maneja casos de conexión lenta o sin conexión

---

## 📞 Contacto y Soporte

Para dudas o problemas con la API:

- Consultar `rules.md` - Documentación técnica del backend
- Consultar `GUIA_ENDPOINTS_CLIENTE.md` - Ejemplos con curl

---

**Versión:** 1.0  
**Última actualización:** 2025-10-26  
**Estado:** ✅ Producción

