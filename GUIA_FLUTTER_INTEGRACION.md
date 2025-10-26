# 📱 Guía de Integración Flutter - Burritos To Go API

## 🌐 Información de Conexión

### URLs de Producción
```dart
// PythonAnywhere (Producción)
const String BASE_URL = 'https://pradodiazbackend.pythonanywhere.com/api/';

// Local (Desarrollo)
const String BASE_URL_LOCAL = 'http://127.0.0.1:8000/api/';
```

---

## 🔐 Sistema de Autenticación

### 1. Login con Token

**Endpoint:** `POST /api/token/`

**Request:**
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<String?> login(String username, String password) async {
  final url = Uri.parse('${BASE_URL}token/');
  
  try {
    final response = await http.post(
      url,
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['token']; // Guardar este token
    } else {
      print('Error: ${response.body}');
      return null;
    }
  } catch (e) {
    print('Exception: $e');
    return null;
  }
}
```

**Response exitosa (200):**
```json
{
  "token": "9d8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f"
}
```

**Response error (400):**
```json
{
  "non_field_errors": ["Unable to log in with provided credentials."]
}
```

### Usuarios de prueba:
```
Cliente:
  username: cliente
  password: cliente123

Admin:
  username: admin
  password: admin123
```

---

## 📋 Endpoints para Cliente

### 1. Ver Menú de Productos

**Endpoint:** `GET /api/menu/`  
**Autenticación:** Requerida

```dart
Future<List<dynamic>> obtenerMenu(String token) async {
  final url = Uri.parse('${BASE_URL}menu/');
  
  final response = await http.get(
    url,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Token $token',
    },
  );
  
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Error al cargar menú');
  }
}
```

**Response:**
```json
[
  {
    "id": 1,
    "nombre": "Burrito de Carne",
    "descripcion": "Delicioso burrito con carne de res",
    "precio": "75.00",
    "disponible": true,
    "imagen": null
  },
  {
    "id": 2,
    "nombre": "Burrito de Pollo",
    "descripcion": "Burrito con pollo marinado",
    "precio": "65.00",
    "disponible": true,
    "imagen": null
  }
]
```

---

### 2. Consultar Saldo

**Endpoint:** `GET /api/mi-saldo/`  
**Autenticación:** Requerida

```dart
Future<double> obtenerSaldo(String token) async {
  final url = Uri.parse('${BASE_URL}mi-saldo/');
  
  final response = await http.get(
    url,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Token $token',
    },
  );
  
  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    return double.parse(data['saldo'].toString());
  } else {
    throw Exception('Error al obtener saldo');
  }
}
```

**Response:**
```json
{
  "usuario": "cliente",
  "saldo": "500.00"
}
```

---

### 3. Recargar Saldo

**Endpoint:** `POST /api/recargar-saldo/`  
**Autenticación:** Requerida

```dart
Future<bool> recargarSaldo(String token, double monto) async {
  final url = Uri.parse('${BASE_URL}recargar-saldo/');
  
  final response = await http.post(
    url,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Token $token',
    },
    body: jsonEncode({
      'monto': monto,
    }),
  );
  
  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    print('Nuevo saldo: ${data['nuevo_saldo']}');
    return true;
  } else {
    print('Error: ${response.body}');
    return false;
  }
}
```

**Request:**
```json
{
  "monto": 100.50
}
```

**Response exitosa:**
```json
{
  "mensaje": "Saldo recargado exitosamente",
  "nuevo_saldo": "600.50"
}
```

**Response error:**
```json
{
  "error": "El monto debe ser mayor a cero"
}
```

---

### 4. Crear Pedido

**Endpoint:** `POST /api/pedidos/`  
**Autenticación:** Requerida

```dart
class ItemPedido {
  final int productoId;
  final int cantidad;
  
  ItemPedido({required this.productoId, required this.cantidad});
  
  Map<String, dynamic> toJson() => {
    'producto_id': productoId,
    'cantidad': cantidad,
  };
}

Future<Map<String, dynamic>?> crearPedido(
  String token, 
  List<ItemPedido> items
) async {
  final url = Uri.parse('${BASE_URL}pedidos/');
  
  final response = await http.post(
    url,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Token $token',
    },
    body: jsonEncode({
      'items': items.map((item) => item.toJson()).toList(),
    }),
  );
  
  if (response.statusCode == 201) {
    return jsonDecode(response.body);
  } else {
    print('Error: ${response.body}');
    return null;
  }
}
```

**Request:**
```json
{
  "items": [
    {
      "producto_id": 1,
      "cantidad": 2
    },
    {
      "producto_id": 3,
      "cantidad": 1
    }
  ]
}
```

**Response exitosa (201):**
```json
{
  "id": 5,
  "cliente": {
    "id": 2,
    "username": "cliente",
    "nombre": "Cliente Demo"
  },
  "items": [
    {
      "id": 8,
      "producto": {
        "id": 1,
        "nombre": "Burrito de Carne",
        "precio": "75.00"
      },
      "cantidad": 2,
      "subtotal": "150.00"
    },
    {
      "id": 9,
      "producto": {
        "id": 3,
        "nombre": "Quesadilla",
        "precio": "45.00"
      },
      "cantidad": 1,
      "subtotal": "45.00"
    }
  ],
  "total": "195.00",
  "estado": "pendiente",
  "fecha_pedido": "2025-10-26T20:30:00Z",
  "saldo_restante": "305.00"
}
```

**Response error (400):**
```json
{
  "error": "Saldo insuficiente. Necesitas $195.00 pero tienes $100.00"
}
```

---

### 5. Consultar Mis Pedidos

**Endpoint:** `GET /api/mis-pedidos/`  
**Autenticación:** Requerida

```dart
Future<List<dynamic>> obtenerMisPedidos(String token) async {
  final url = Uri.parse('${BASE_URL}mis-pedidos/');
  
  final response = await http.get(
    url,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Token $token',
    },
  );
  
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Error al cargar pedidos');
  }
}
```

**Response:**
```json
[
  {
    "id": 5,
    "items": [
      {
        "producto": {
          "nombre": "Burrito de Carne"
        },
        "cantidad": 2,
        "subtotal": "150.00"
      }
    ],
    "total": "195.00",
    "estado": "pendiente",
    "fecha_pedido": "2025-10-26T20:30:00Z"
  },
  {
    "id": 4,
    "items": [
      {
        "producto": {
          "nombre": "Burrito de Pollo"
        },
        "cantidad": 1,
        "subtotal": "65.00"
      }
    ],
    "total": "65.00",
    "estado": "completado",
    "fecha_pedido": "2025-10-25T18:15:00Z"
  }
]
```

---

### 6. Ver Detalle de Pedido

**Endpoint:** `GET /api/pedido/<id>/`  
**Autenticación:** Requerida

```dart
Future<Map<String, dynamic>> obtenerDetallePedido(
  String token, 
  int pedidoId
) async {
  final url = Uri.parse('${BASE_URL}pedido/$pedidoId/');
  
  final response = await http.get(
    url,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Token $token',
    },
  );
  
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Error al cargar detalle');
  }
}
```

---

## 👨‍💼 Endpoints para Administrador

### 1. Listar Todos los Pedidos

**Endpoint:** `GET /api/pedidos-admin/`  
**Autenticación:** Requerida (Admin)

```dart
Future<List<dynamic>> obtenerTodosPedidos(String token) async {
  final url = Uri.parse('${BASE_URL}pedidos-admin/');
  
  final response = await http.get(
    url,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Token $token',
    },
  );
  
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else if (response.statusCode == 403) {
    throw Exception('No tienes permisos de administrador');
  } else {
    throw Exception('Error al cargar pedidos');
  }
}
```

---

### 2. Gestión de Productos (CRUD)

**Listar productos:**
```dart
GET /api/productos/
```

**Crear producto:**
```dart
POST /api/productos/
Body: {
  "nombre": "Nuevo Burrito",
  "descripcion": "Descripción",
  "precio": 80.00,
  "disponible": true
}
```

**Actualizar producto:**
```dart
PUT /api/productos/{id}/
```

**Eliminar producto:**
```dart
DELETE /api/productos/{id}/
```

---

## 🛡️ Manejo de Errores

```dart
class ApiService {
  Future<dynamic> handleResponse(http.Response response) async {
    switch (response.statusCode) {
      case 200:
      case 201:
        return jsonDecode(response.body);
      
      case 400:
        final error = jsonDecode(response.body);
        throw Exception(error['error'] ?? 'Error en la solicitud');
      
      case 401:
        throw Exception('No autenticado. Inicia sesión nuevamente');
      
      case 403:
        throw Exception('No tienes permisos para esta acción');
      
      case 404:
        throw Exception('Recurso no encontrado');
      
      case 500:
        throw Exception('Error del servidor. Intenta más tarde');
      
      default:
        throw Exception('Error desconocido: ${response.statusCode}');
    }
  }
}
```

---

## 📦 Modelo de Datos Flutter

```dart
// Producto
class Producto {
  final int id;
  final String nombre;
  final String descripcion;
  final double precio;
  final bool disponible;
  
  Producto({
    required this.id,
    required this.nombre,
    required this.descripcion,
    required this.precio,
    required this.disponible,
  });
  
  factory Producto.fromJson(Map<String, dynamic> json) {
    return Producto(
      id: json['id'],
      nombre: json['nombre'],
      descripcion: json['descripcion'],
      precio: double.parse(json['precio'].toString()),
      disponible: json['disponible'],
    );
  }
}

// Pedido
class Pedido {
  final int id;
  final List<ItemPedido> items;
  final double total;
  final String estado;
  final DateTime fechaPedido;
  
  Pedido({
    required this.id,
    required this.items,
    required this.total,
    required this.estado,
    required this.fechaPedido,
  });
  
  factory Pedido.fromJson(Map<String, dynamic> json) {
    return Pedido(
      id: json['id'],
      items: (json['items'] as List)
          .map((item) => ItemPedido.fromJson(item))
          .toList(),
      total: double.parse(json['total'].toString()),
      estado: json['estado'],
      fechaPedido: DateTime.parse(json['fecha_pedido']),
    );
  }
}
```

---

## 🔄 Estados de Pedido

```dart
enum EstadoPedido {
  pendiente,
  en_preparacion,
  listo,
  entregado,
  cancelado
}

String getEstadoTexto(String estado) {
  switch (estado) {
    case 'pendiente':
      return '⏳ Pendiente';
    case 'en_preparacion':
      return '👨‍🍳 En Preparación';
    case 'listo':
      return '✅ Listo';
    case 'entregado':
      return '🎉 Entregado';
    case 'cancelado':
      return '❌ Cancelado';
    default:
      return estado;
  }
}
```

---

## ✅ Checklist de Integración

- [ ] Configurar URL base de producción
- [ ] Implementar sistema de login
- [ ] Guardar token de forma segura (SharedPreferences)
- [ ] Implementar vista de menú
- [ ] Implementar carrito de compras
- [ ] Implementar creación de pedidos
- [ ] Implementar vista de pedidos históricos
- [ ] Implementar recarga de saldo
- [ ] Implementar manejo de errores
- [ ] Probar con usuarios de prueba
- [ ] Implementar logout
- [ ] Implementar refresh de token si es necesario

---

## 🎯 URLs de Acceso

**Producción:**
- API Base: https://pradodiazbackend.pythonanywhere.com/api/
- Admin Panel: https://pradodiazbackend.pythonanywhere.com/admin/
- Dashboard: https://pradodiazbackend.pythonanywhere.com/api/panel/

**Credenciales de prueba:**
```
Cliente:
  username: cliente
  password: cliente123

Admin:
  username: admin
  password: admin123
```

---

## 📞 Soporte

Para cualquier duda sobre la integración, revisar:
- `DOCUMENTACION_API_FLUTTER.md` - Documentación completa de la API
- `GUIA_ENDPOINTS_CLIENTE.md` - Guía específica de endpoints para cliente
- Repositorio: https://github.com/BernardoPD/burritos-to-go-api

---

¡Tu API está lista para ser consumida desde Flutter! 🎉
