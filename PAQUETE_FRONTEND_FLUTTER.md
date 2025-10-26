# 📦 Paquete de Entrega para Frontend (Flutter)

**Fecha de entrega:** 2025-10-26  
**Backend:** Django REST Framework  
**Versión API:** 1.0  
**Estado:** ✅ DESPLEGADO EN PRODUCCIÓN

**URL Producción:** https://pradodiazbackend.pythonanywhere.com

---

## 📋 Archivos Incluidos

| Archivo | Descripción |
|---------|-------------|
| `GUIA_FLUTTER_INTEGRACION.md` | **⭐ EMPEZAR AQUÍ** - Código Flutter completo con ejemplos |
| `DOCUMENTACION_API_FLUTTER.md` | Documentación completa con ejemplos en Dart |
| `GUIA_ENDPOINTS_CLIENTE.md` | Endpoints específicos para la app cliente |
| `DEPLOYMENT_PASO_A_PASO.md` | Guía de deployment en PythonAnywhere |
| `Burritos_API_Collection.postman_collection.json` | Colección de Postman para probar endpoints |
| Este archivo | Resumen ejecutivo |

---

## 🚀 Quick Start

### 1. URL Base de la API

**PRODUCCIÓN (Usar esta):**
```dart
const String BASE_URL = 'https://pradodiazbackend.pythonanywhere.com/api/';
```

**Local (solo para desarrollo):**
```dart
const String BASE_URL_LOCAL = 'http://127.0.0.1:8000/api/';
```

---

### 2. Endpoints Principales

#### 🔐 Autenticación
```dart
// Login
POST /api/auth/login/
Body: {"username": "cliente", "password": "cliente123"}
Response: {"token": "...", "usuario": {...}}

// Registro
POST /api/auth/register/
Body: {"username": "...", "email": "...", "password": "...", "password2": "..."}
```

#### 👤 Cliente
```dart
// Ver menú (público)
GET /api/cliente/menu/

// Mis pedidos
GET /api/cliente/mis-pedidos/
GET /api/cliente/mis-pedidos/?tipo=actuales
GET /api/cliente/mis-pedidos/?tipo=pasados

// Mi saldo
GET /api/cliente/mi-saldo/

// Recargar saldo
POST /api/cliente/recargar-saldo/
Body: {"monto": 100.00}

// Crear pedido
POST /api/crear_pedido/
Body: {"productos": [1, 5]}
```

---

## 🔑 Autenticación con Token

Después del login, guardar el token y usarlo en todas las peticiones protegidas:

```dart
headers: {
  'Authorization': 'Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b',
  'Content-Type': 'application/json'
}
```

---

## 📱 Usuarios de Prueba

### Cliente
```
Username: cliente
Password: cliente123
Saldo: $600
```

### Admin
```
Username: admin
Password: admin123
Saldo: $380
```

---

## 🧪 Probar la API

### Opción 1: Con Postman

1. Importar el archivo `Burritos_API_Collection.postman_collection.json`
2. En Variables de entorno, configurar:
   - `base_url` = `http://localhost:8000/api`
   - `token` = *(se obtiene después del login)*
3. Ejecutar "Login" primero
4. Copiar el token del response
5. Pegar en la variable `token`
6. Probar los demás endpoints

### Opción 2: Con curl

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"cliente","password":"cliente123"}'

# Ver menú
curl http://localhost:8000/api/cliente/menu/

# Crear pedido
curl -X POST http://localhost:8000/api/crear_pedido/ \
  -H "Authorization: Token TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"productos":[1,5]}'
```

---

## 📊 Flujos Principales

### Flujo 1: Registro y Login

```
Usuario registra cuenta
  ↓
POST /api/auth/register/
  ↓
Recibe token automáticamente
  ↓
Guardar token en SharedPreferences
  ↓
Listo para usar la app
```

### Flujo 2: Login Existente

```
Usuario ingresa credenciales
  ↓
POST /api/auth/login/
  ↓
Recibe token
  ↓
Guardar token
  ↓
Redirigir a dashboard
```

### Flujo 3: Hacer Pedido

```
Ver menú (GET /api/cliente/menu/)
  ↓
Seleccionar productos
  ↓
Verificar saldo (GET /api/cliente/mi-saldo/)
  ↓
Crear pedido (POST /api/crear_pedido/)
  ↓
Saldo se descuenta automáticamente
  ↓
Mostrar confirmación
```

### Flujo 4: Recargar Saldo

```
Ver saldo actual (GET /api/cliente/mi-saldo/)
  ↓
Ingresar monto a recargar
  ↓
POST /api/cliente/recargar-saldo/
  ↓
Saldo se actualiza inmediatamente
  ↓
Mostrar nuevo saldo
```

---

## 🎨 Modelos de Datos para Flutter

### Usuario
```dart
class Usuario {
  final int id;
  final String username;
  final String email;
  final String? firstName;
  final String? lastName;
  final String rol;
  final double saldo;
  final DateTime dateJoined;

  Usuario({
    required this.id,
    required this.username,
    required this.email,
    this.firstName,
    this.lastName,
    required this.rol,
    required this.saldo,
    required this.dateJoined,
  });

  factory Usuario.fromJson(Map<String, dynamic> json) {
    return Usuario(
      id: json['id'],
      username: json['username'],
      email: json['email'],
      firstName: json['first_name'],
      lastName: json['last_name'],
      rol: json['rol'],
      saldo: double.parse(json['saldo'].toString()),
      dateJoined: DateTime.parse(json['date_joined']),
    );
  }
}
```

### Producto
```dart
class Producto {
  final int id;
  final String nombre;
  final String descripcion;
  final double precio;
  final int categoria;
  final String categoriaNombre;
  final bool activo;

  Producto({
    required this.id,
    required this.nombre,
    required this.descripcion,
    required this.precio,
    required this.categoria,
    required this.categoriaNombre,
    required this.activo,
  });

  factory Producto.fromJson(Map<String, dynamic> json) {
    return Producto(
      id: json['id'],
      nombre: json['nombre'],
      descripcion: json['descripcion'],
      precio: double.parse(json['precio'].toString()),
      categoria: json['categoria'],
      categoriaNombre: json['categoria_nombre'],
      activo: json['activo'],
    );
  }
}
```

### Pedido
```dart
class Pedido {
  final int id;
  final int cliente;
  final String clienteNombre;
  final List<ProductoDetalle> productosDetalle;
  final double total;
  final String estatus;
  final DateTime fecha;

  Pedido({
    required this.id,
    required this.cliente,
    required this.clienteNombre,
    required this.productosDetalle,
    required this.total,
    required this.estatus,
    required this.fecha,
  });

  factory Pedido.fromJson(Map<String, dynamic> json) {
    return Pedido(
      id: json['id'],
      cliente: json['cliente'],
      clienteNombre: json['cliente_nombre'],
      productosDetalle: (json['productos_detalle'] as List)
          .map((p) => ProductoDetalle.fromJson(p))
          .toList(),
      total: double.parse(json['total'].toString()),
      estatus: json['estatus'],
      fecha: DateTime.parse(json['fecha']),
    );
  }
}

class ProductoDetalle {
  final int id;
  final String nombre;
  final double precio;

  ProductoDetalle({
    required this.id,
    required this.nombre,
    required this.precio,
  });

  factory ProductoDetalle.fromJson(Map<String, dynamic> json) {
    return ProductoDetalle(
      id: json['id'],
      nombre: json['nombre'],
      precio: double.parse(json['precio'].toString()),
    );
  }
}
```

---

## ⚠️ Errores Comunes

### 1. Error 401 - Unauthorized
```json
{"detail": "Authentication credentials were not provided."}
```
**Solución:** Incluir header `Authorization: Token <token>`

### 2. Error 400 - Saldo Insuficiente
```json
{
  "error": "Saldo insuficiente.",
  "saldo_actual": 50.0,
  "total_pedido": 100.0,
  "faltante": 50.0
}
```
**Solución:** Mostrar mensaje al usuario para recargar saldo

### 3. Error 400 - Productos Inválidos
```json
{"error": "No se encontraron productos válidos."}
```
**Solución:** Verificar que los IDs de productos existan y estén activos

---

## 🔒 Seguridad

### 1. Almacenamiento del Token

```dart
import 'package:shared_preferences/shared_preferences.dart';

// Guardar token
Future<void> guardarToken(String token) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setString('auth_token', token);
}

// Obtener token
Future<String?> obtenerToken() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString('auth_token');
}

// Eliminar token (logout)
Future<void> eliminarToken() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.remove('auth_token');
}
```

### 2. Interceptor HTTP

```dart
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api';
  
  Future<http.Response> get(String endpoint) async {
    final token = await obtenerToken();
    return http.get(
      Uri.parse('$baseUrl$endpoint'),
      headers: {
        'Authorization': 'Token $token',
        'Content-Type': 'application/json',
      },
    );
  }
}
```

---

## 📞 Contacto

**Backend Developer:** GitHub Copilot Assistant  
**Fecha:** 2025-10-26

**Archivos de documentación:**
- `DOCUMENTACION_API_FLUTTER.md` - Documentación completa
- `rules.md` - Reglas y arquitectura del backend
- `GUIA_ENDPOINTS_CLIENTE.md` - Guía con ejemplos curl

---

## ✅ Checklist para Frontend

- [ ] Importar colección de Postman
- [ ] Probar todos los endpoints principales
- [ ] Crear modelos de datos en Dart
- [ ] Implementar servicio de API
- [ ] Implementar almacenamiento de token
- [ ] Manejar errores 400, 401, 404
- [ ] Implementar flujo de login/registro
- [ ] Implementar flujo de pedidos
- [ ] Implementar recarga de saldo
- [ ] Implementar vista de mis pedidos

---

**¡Listo para integrar con Flutter!** 🚀
