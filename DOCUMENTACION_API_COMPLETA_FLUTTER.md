# 📱 Documentación Completa de API - Burritos To Go
## Para Integración con Flutter / Frontend

---

## 📋 Tabla de Contenidos

1. [Información General](#información-general)
2. [Base URL](#base-url)
3. [Autenticación](#autenticación)
4. [Endpoints de Autenticación](#endpoints-de-autenticación)
5. [Endpoints para Clientes](#endpoints-para-clientes)
6. [Endpoints para Administradores](#endpoints-para-administradores)
7. [Modelos de Datos](#modelos-de-datos)
8. [Códigos de Estado HTTP](#códigos-de-estado-http)
9. [Ejemplos de Integración](#ejemplos-de-integración)

---

## 📌 Información General

**Sistema:** Burritos To Go - API REST  
**Framework:** Django REST Framework  
**Base de Datos:** MySQL  
**Autenticación:** Token Authentication  

### Funcionalidades por Rol

#### 👤 Cliente puede:
- ✅ Registrarse en el sistema
- ✅ Iniciar sesión
- ✅ Consultar menú completo
- ✅ Hacer pedidos
- ✅ Consultar sus pedidos (actuales y pasados)
- ✅ Consultar su saldo
- ✅ Recargar saldo a su cuenta

#### 👨‍💼 Administrador puede:
- ✅ Gestionar usuarios (CRUD)
- ✅ Gestionar productos (CRUD)
- ✅ Gestionar categorías (CRUD)
- ✅ Gestionar pedidos (CRUD)
- ✅ Ver estadísticas del sistema

---

## 🌐 Base URL

### Local (Desarrollo)
```
http://localhost:8000/api/
```

### Producción (PythonAnywhere)
```
https://pradodiazbackend.pythonanywhere.com/api/
```

---

## 🔐 Autenticación

El sistema usa **Token Authentication** de Django REST Framework.

### ¿Cómo funciona?

1. **Registrarse o Login** → Recibes un `token`
2. **Incluir el token** en todas las peticiones protegidas

### Headers requeridos para endpoints protegidos

```http
Authorization: Token <tu_token_aqui>
Content-Type: application/json
```

### Ejemplo en diferentes lenguajes

#### JavaScript (Fetch)
```javascript
fetch('http://localhost:8000/api/cliente/mi-saldo/', {
  method: 'GET',
  headers: {
    'Authorization': 'Token abc123xyz',
    'Content-Type': 'application/json'
  }
})
```

#### Flutter (Dart)
```dart
import 'package:http/http.dart' as http;

var response = await http.get(
  Uri.parse('http://localhost:8000/api/cliente/mi-saldo/'),
  headers: {
    'Authorization': 'Token abc123xyz',
    'Content-Type': 'application/json'
  },
);
```

#### Python (requests)
```python
import requests

headers = {
    'Authorization': 'Token abc123xyz',
    'Content-Type': 'application/json'
}

response = requests.get(
    'http://localhost:8000/api/cliente/mi-saldo/',
    headers=headers
)
```

---

## 🔑 Endpoints de Autenticación

### 1. Registro de Usuario

**Endpoint:** `POST /api/auth/register/`  
**Autenticación:** No requerida  

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

**Respuesta Exitosa (201 Created):**
```json
{
  "mensaje": "Usuario registrado exitosamente",
  "token": "abc123xyz456def789",
  "usuario": {
    "id": 5,
    "username": "cliente1",
    "email": "cliente1@example.com",
    "rol": "cliente",
    "saldo": 0.0
  }
}
```

**Respuesta Error (400 Bad Request):**
```json
{
  "error": "Datos inválidos",
  "detalles": {
    "username": ["Este nombre de usuario ya existe"],
    "email": ["Este email ya está registrado"],
    "password2": ["Las contraseñas no coinciden"]
  }
}
```

**Validaciones:**
- Username único
- Email único y válido
- Password mínimo 6 caracteres
- password y password2 deben coincidir

---

### 2. Login (Iniciar Sesión)

**Endpoint:** `POST /api/auth/login/`  
**Autenticación:** No requerida  

**Body:**
```json
{
  "username": "cliente",
  "password": "cliente123"
}
```

**Respuesta Exitosa (200 OK):**
```json
{
  "mensaje": "Login exitoso",
  "token": "4b299407e0f84fd583a1aa029676fe51884b1b48",
  "usuario": {
    "id": 2,
    "username": "cliente",
    "email": "cliente@example.com",
    "rol": "cliente",
    "saldo": 500.0
  }
}
```

**Respuesta Error (400 Bad Request):**
```json
{
  "error": "Datos inválidos",
  "detalles": {
    "non_field_errors": ["Credenciales inválidas"]
  }
}
```

---

### 3. Cerrar Sesión

**Endpoint:** `POST /api/auth/logout/`  
**Autenticación:** Requerida (Token)  

**Headers:**
```http
Authorization: Token abc123xyz
```

**Respuesta Exitosa (200 OK):**
```json
{
  "mensaje": "Sesión cerrada exitosamente"
}
```

---

### 4. Mi Perfil

**Endpoint:** `GET /api/auth/mi-perfil/`  
**Autenticación:** Requerida (Token)  

**Respuesta Exitosa (200 OK):**
```json
{
  "id": 2,
  "username": "cliente",
  "email": "cliente@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "rol": "cliente",
  "saldo": 500.0,
  "date_joined": "2025-01-15T10:30:00Z"
}
```

---

## 🍔 Endpoints para Clientes

### 1. Consultar Menú

**Endpoint:** `GET /api/cliente/menu/`  
**Autenticación:** No requerida  

**Descripción:** Muestra el menú completo organizado por categorías con productos activos.

**Respuesta Exitosa (200 OK):**
```json
{
  "categorias": [
    {
      "id": 1,
      "nombre": "Burritos",
      "productos": [
        {
          "id": 1,
          "nombre": "Burrito de Carne",
          "descripcion": "Delicioso burrito con carne asada",
          "precio": "80.00",
          "categoria_nombre": "Burritos"
        },
        {
          "id": 2,
          "nombre": "Burrito Vegetariano",
          "descripcion": "Burrito con vegetales frescos",
          "precio": "70.00",
          "categoria_nombre": "Burritos"
        }
      ]
    },
    {
      "id": 2,
      "nombre": "Bebidas",
      "productos": [
        {
          "id": 3,
          "nombre": "Refresco",
          "descripcion": "Refresco de 355ml",
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

### 2. Hacer Pedido

**Endpoint:** `POST /api/crear_pedido/`  
**Autenticación:** Requerida (Token)  

**Body:**
```json
{
  "productos": [1, 3]
}
```

**Respuesta Exitosa (200 OK):**
```json
{
  "mensaje": "Pedido creado exitosamente.",
  "pedido_id": 10,
  "total": 100.00,
  "productos": [
    "Burrito de Carne",
    "Refresco"
  ],
  "fecha": "2025-10-26T19:30:00Z",
  "saldo_restante": 400.00
}
```

**Respuesta Error - Saldo Insuficiente (400 Bad Request):**
```json
{
  "error": "Saldo insuficiente.",
  "saldo_actual": 50.00,
  "total_pedido": 100.00,
  "faltante": 50.00
}
```

**Respuesta Error - Productos Inválidos (400 Bad Request):**
```json
{
  "error": "No se encontraron productos válidos."
}
```

**⚠️ IMPORTANTE:**
- Se valida que el cliente tenga saldo suficiente
- Se descuenta automáticamente el total del pedido del saldo del cliente
- Los productos deben existir y estar activos
- El total se calcula automáticamente en el backend

---

### 3. Consultar Mis Pedidos

**Endpoint:** `GET /api/cliente/mis-pedidos/`  
**Autenticación:** Requerida (Token)  

**Parámetros de consulta (opcionales):**
- `?tipo=actuales` - Solo pedidos pendientes o en proceso
- `?tipo=pasados` - Solo pedidos completados o cancelados
- `?estatus=pendiente` - Filtrar por estatus específico

**Ejemplos:**
```
GET /api/cliente/mis-pedidos/
GET /api/cliente/mis-pedidos/?tipo=actuales
GET /api/cliente/mis-pedidos/?tipo=pasados
GET /api/cliente/mis-pedidos/?estatus=pendiente
```

**Respuesta Exitosa (200 OK):**
```json
{
  "pedidos": [
    {
      "id": 10,
      "cliente": 2,
      "cliente_nombre": "cliente",
      "productos_detalle": [
        {
          "id": 1,
          "nombre": "Burrito de Carne",
          "precio": 80.0
        },
        {
          "id": 3,
          "nombre": "Refresco",
          "precio": 20.0
        }
      ],
      "total": "100.00",
      "estatus": "pendiente",
      "fecha": "2025-10-26T19:30:00Z"
    },
    {
      "id": 9,
      "cliente": 2,
      "cliente_nombre": "cliente",
      "productos_detalle": [
        {
          "id": 2,
          "nombre": "Burrito Vegetariano",
          "precio": 70.0
        }
      ],
      "total": "70.00",
      "estatus": "completado",
      "fecha": "2025-10-25T14:20:00Z"
    }
  ],
  "total": 2,
  "filtros_aplicados": {
    "tipo": null,
    "estatus": null
  }
}
```

**Estatus posibles:**
- `pendiente` - Pedido recién creado
- `en_proceso` - Pedido en preparación
- `completado` - Pedido entregado
- `cancelado` - Pedido cancelado

---

### 4. Consultar Mi Saldo

**Endpoint:** `GET /api/cliente/mi-saldo/`  
**Autenticación:** Requerida (Token)  

**Respuesta Exitosa (200 OK):**
```json
{
  "saldo": 500.0,
  "usuario": "cliente",
  "email": "cliente@example.com",
  "fecha_consulta": "2025-10-26T19:30:00Z"
}
```

---

### 5. Recargar Saldo

**Endpoint:** `POST /api/cliente/recargar-saldo/`  
**Autenticación:** Requerida (Token)  

**Body:**
```json
{
  "monto": 100.00
}
```

**Validaciones:**
- Monto mínimo: $0.01
- Monto máximo: $10,000.00
- Debe ser un número decimal válido

**Respuesta Exitosa (200 OK):**
```json
{
  "mensaje": "Saldo recargado exitosamente",
  "monto_recargado": 100.0,
  "saldo_anterior": 500.0,
  "saldo_actual": 600.0,
  "usuario": "cliente",
  "fecha_recarga": "2025-10-26T19:35:00Z"
}
```

**Respuesta Error (400 Bad Request):**
```json
{
  "error": "Datos inválidos",
  "detalles": {
    "monto": ["El monto debe ser mayor a 0"]
  }
}
```

---

## 👨‍💼 Endpoints para Administradores

### 1. Gestión de Usuarios

#### Listar Usuarios
**Endpoint:** `GET /api/usuarios/`  
**Autenticación:** Requerida (Admin)  

**Respuesta:**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "rol": "admin",
    "saldo": 0.0
  },
  {
    "id": 2,
    "username": "cliente",
    "email": "cliente@example.com",
    "rol": "cliente",
    "saldo": 500.0
  }
]
```

#### Ver Usuario
**Endpoint:** `GET /api/usuarios/{id}/`  
**Autenticación:** Requerida (Admin)  

#### Crear Usuario
**Endpoint:** `POST /api/usuarios/`  
**Autenticación:** Requerida (Admin)  

#### Actualizar Usuario
**Endpoint:** `PUT /api/usuarios/{id}/`  
**Autenticación:** Requerida (Admin)  

#### Eliminar Usuario
**Endpoint:** `DELETE /api/usuarios/{id}/`  
**Autenticación:** Requerida (Admin)  

---

### 2. Gestión de Productos

#### Listar Productos
**Endpoint:** `GET /api/productos/`  
**Autenticación:** No requerida  

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Burrito de Carne",
    "descripcion": "Delicioso burrito con carne asada",
    "precio": "80.00",
    "categoria": 1,
    "categoria_nombre": "Burritos",
    "activo": true
  }
]
```

#### Ver Producto
**Endpoint:** `GET /api/productos/{id}/`  

#### Crear Producto
**Endpoint:** `POST /api/productos/`  
**Autenticación:** Requerida (Admin)  

**Body:**
```json
{
  "nombre": "Nuevo Burrito",
  "descripcion": "Descripción del burrito",
  "precio": "85.00",
  "categoria": 1,
  "activo": true
}
```

#### Actualizar Producto
**Endpoint:** `PUT /api/productos/{id}/`  
**Autenticación:** Requerida (Admin)  

#### Eliminar Producto (Soft Delete)
**Endpoint:** `DELETE /api/productos/{id}/`  
**Autenticación:** Requerida (Admin)  

---

### 3. Gestión de Categorías

#### Listar Categorías
**Endpoint:** `GET /api/categorias/`  

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Burritos"
  },
  {
    "id": 2,
    "nombre": "Bebidas"
  }
]
```

#### Ver Categoría
**Endpoint:** `GET /api/categorias/{id}/`  

#### Crear Categoría
**Endpoint:** `POST /api/categorias/`  
**Autenticación:** Requerida (Admin)  

**Body:**
```json
{
  "nombre": "Postres"
}
```

#### Actualizar Categoría
**Endpoint:** `PUT /api/categorias/{id}/`  
**Autenticación:** Requerida (Admin)  

#### Eliminar Categoría
**Endpoint:** `DELETE /api/categorias/{id}/`  
**Autenticación:** Requerida (Admin)  

---

### 4. Gestión de Pedidos

#### Listar Pedidos
**Endpoint:** `GET /api/pedidos/`  
**Autenticación:** Requerida (Admin)  

**Respuesta:**
```json
[
  {
    "id": 10,
    "cliente": 2,
    "productos": [1, 3],
    "total": "100.00",
    "estatus": "pendiente",
    "fecha": "2025-10-26T19:30:00Z"
  }
]
```

#### Ver Pedido
**Endpoint:** `GET /api/pedidos/{id}/`  
**Autenticación:** Requerida (Admin)  

#### Crear Pedido (Admin)
**Endpoint:** `POST /api/pedidos/`  
**Autenticación:** Requerida (Admin)  

**Body:**
```json
{
  "productos": [1, 2, 3],
  "estatus": "pendiente"
}
```

**⚠️ IMPORTANTE:**
- El campo `cliente` se toma automáticamente del usuario autenticado
- El campo `total` se calcula automáticamente
- Se valida saldo suficiente del cliente
- Se descuenta automáticamente del saldo del cliente

#### Actualizar Pedido
**Endpoint:** `PUT /api/pedidos/{id}/`  
**Autenticación:** Requerida (Admin)  

**Body:**
```json
{
  "estatus": "completado"
}
```

#### Eliminar Pedido
**Endpoint:** `DELETE /api/pedidos/{id}/`  
**Autenticación:** Requerida (Admin)  

---

## 📊 Modelos de Datos

### Usuario
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "rol": "cliente|admin|super",
  "saldo": "decimal",
  "date_joined": "datetime"
}
```

### Producto
```json
{
  "id": 1,
  "nombre": "string",
  "descripcion": "string",
  "precio": "decimal",
  "categoria": 1,
  "categoria_nombre": "string",
  "activo": true
}
```

### Categoría
```json
{
  "id": 1,
  "nombre": "string"
}
```

### Pedido
```json
{
  "id": 1,
  "cliente": 2,
  "productos": [1, 2, 3],
  "total": "decimal",
  "estatus": "pendiente|en_proceso|completado|cancelado",
  "fecha": "datetime"
}
```

---

## 🔢 Códigos de Estado HTTP

| Código | Significado | Cuándo se usa |
|--------|-------------|---------------|
| 200 | OK | Solicitud exitosa (GET, PUT, PATCH) |
| 201 | Created | Recurso creado exitosamente (POST) |
| 400 | Bad Request | Datos inválidos o faltantes |
| 401 | Unauthorized | No autenticado (falta token o es inválido) |
| 403 | Forbidden | No tiene permisos para esta acción |
| 404 | Not Found | Recurso no encontrado |
| 500 | Server Error | Error interno del servidor |

---

## 💡 Ejemplos de Integración

### Flujo Completo en Flutter (Dart)

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class BurritosAPI {
  static const String baseURL = 'http://localhost:8000/api';
  String? authToken;
  
  // 1. REGISTRO
  Future<Map<String, dynamic>> register(
    String username,
    String email,
    String password,
    String firstName,
    String lastName
  ) async {
    final response = await http.post(
      Uri.parse('$baseURL/auth/register/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'email': email,
        'password': password,
        'password2': password,
        'first_name': firstName,
        'last_name': lastName,
      }),
    );
    
    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      authToken = data['token'];
      return data;
    } else {
      throw Exception('Error en registro: ${response.body}');
    }
  }
  
  // 2. LOGIN
  Future<Map<String, dynamic>> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseURL/auth/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      authToken = data['token'];
      return data;
    } else {
      throw Exception('Error en login: ${response.body}');
    }
  }
  
  // 3. CONSULTAR MENÚ
  Future<Map<String, dynamic>> getMenu() async {
    final response = await http.get(
      Uri.parse('$baseURL/cliente/menu/'),
      headers: {'Content-Type': 'application/json'},
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Error al obtener menú');
    }
  }
  
  // 4. CONSULTAR SALDO
  Future<Map<String, dynamic>> getMiSaldo() async {
    final response = await http.get(
      Uri.parse('$baseURL/cliente/mi-saldo/'),
      headers: {
        'Authorization': 'Token $authToken',
        'Content-Type': 'application/json',
      },
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Error al obtener saldo');
    }
  }
  
  // 5. RECARGAR SALDO
  Future<Map<String, dynamic>> recargarSaldo(double monto) async {
    final response = await http.post(
      Uri.parse('$baseURL/cliente/recargar-saldo/'),
      headers: {
        'Authorization': 'Token $authToken',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({'monto': monto}),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Error al recargar saldo: ${response.body}');
    }
  }
  
  // 6. HACER PEDIDO
  Future<Map<String, dynamic>> crearPedido(List<int> productosIds) async {
    final response = await http.post(
      Uri.parse('$baseURL/crear_pedido/'),
      headers: {
        'Authorization': 'Token $authToken',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({'productos': productosIds}),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Error al crear pedido: ${response.body}');
    }
  }
  
  // 7. CONSULTAR MIS PEDIDOS
  Future<Map<String, dynamic>> getMisPedidos({String? tipo, String? estatus}) async {
    String url = '$baseURL/cliente/mis-pedidos/';
    
    // Agregar parámetros de consulta
    List<String> params = [];
    if (tipo != null) params.add('tipo=$tipo');
    if (estatus != null) params.add('estatus=$estatus');
    if (params.isNotEmpty) url += '?${params.join('&')}';
    
    final response = await http.get(
      Uri.parse(url),
      headers: {
        'Authorization': 'Token $authToken',
        'Content-Type': 'application/json',
      },
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Error al obtener pedidos');
    }
  }
  
  // 8. LOGOUT
  Future<void> logout() async {
    await http.post(
      Uri.parse('$baseURL/auth/logout/'),
      headers: {
        'Authorization': 'Token $authToken',
        'Content-Type': 'application/json',
      },
    );
    authToken = null;
  }
}

// EJEMPLO DE USO
void main() async {
  var api = BurritosAPI();
  
  // Login
  var loginData = await api.login('cliente', 'cliente123');
  print('Token: ${loginData['token']}');
  print('Saldo: ${loginData['usuario']['saldo']}');
  
  // Ver menú
  var menu = await api.getMenu();
  print('Categorías: ${menu['total_categorias']}');
  
  // Consultar saldo
  var saldo = await api.getMiSaldo();
  print('Mi saldo: ${saldo['saldo']}');
  
  // Hacer pedido
  var pedido = await api.crearPedido([1, 3]);
  print('Pedido #${pedido['pedido_id']} creado. Total: ${pedido['total']}');
  
  // Ver mis pedidos
  var misPedidos = await api.getMisPedidos();
  print('Total de pedidos: ${misPedidos['total']}');
  
  // Recargar saldo
  var recarga = await api.recargarSaldo(100.00);
  print('Nuevo saldo: ${recarga['saldo_actual']}');
}
```

---

## 🚀 Pasos para Integrar con Flutter

### 1. Agregar dependencias en `pubspec.yaml`
```yaml
dependencies:
  http: ^1.1.0
```

### 2. Crear servicio API (ejemplo arriba)

### 3. Manejar estados y errores
```dart
try {
  var data = await api.login(username, password);
  // Éxito
  Navigator.pushNamed(context, '/dashboard');
} catch (e) {
  // Error
  showDialog(
    context: context,
    builder: (context) => AlertDialog(
      title: Text('Error'),
      content: Text(e.toString()),
    ),
  );
}
```

### 4. Almacenar token localmente
```dart
import 'package:shared_preferences/shared_preferences.dart';

Future<void> saveToken(String token) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setString('auth_token', token);
}

Future<String?> getToken() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString('auth_token');
}
```

---

## 📞 Contacto y Soporte

Para dudas sobre la integración:
- Revisar esta documentación
- Probar endpoints con Postman
- Verificar códigos de error HTTP

---

**Última actualización:** 2025-10-26  
**Versión de API:** 1.0  
**Framework:** Django REST Framework
