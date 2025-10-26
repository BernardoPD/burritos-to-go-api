# 📱 Documentación Completa para Frontend Flutter
## Burritos To Go API

---

## 📋 Tabla de Contenidos
1. [Información General](#información-general)
2. [Base URL y Autenticación](#base-url-y-autenticación)
3. [Endpoints de Autenticación](#endpoints-de-autenticación)
4. [Endpoints para Clientes](#endpoints-para-clientes)
5. [Endpoints para Administradores](#endpoints-para-administradores)
6. [Modelos de Datos](#modelos-de-datos)
7. [Ejemplos de Implementación Flutter](#ejemplos-de-implementación-flutter)
8. [Manejo de Errores](#manejo-de-errores)

---

## 🔗 Información General

**Base URL (Local):** `http://localhost:8000/api/`  
**Base URL (Producción):** `https://pradodiazbackend.pythonanywhere.com/api/`  
**Formato de Respuesta:** JSON  
**Autenticación:** Token Authentication

---

## 🔐 Base URL y Autenticación

### Configuración en Flutter

```dart
class ApiConfig {
  // Cambiar según entorno
  static const String baseUrl = 'https://pradodiazbackend.pythonanywhere.com/api/';
  
  static Map<String, String> headers({String? token}) {
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Token $token',
    };
  }
}
```

---

## 🔑 Endpoints de Autenticación

### 1. Login
**POST** `/api/auth/login/`

**Body:**
```json
{
  "username": "cliente",
  "password": "cliente123"
}
```

**Respuesta Exitosa (200):**
```json
{
  "mensaje": "Login exitoso",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "usuario": {
    "id": 2,
    "username": "cliente",
    "email": "cliente@example.com",
    "rol": "cliente",
    "saldo": 500.00
  }
}
```

**Ejemplo Flutter:**
```dart
Future<Map<String, dynamic>> login(String username, String password) async {
  final response = await http.post(
    Uri.parse('${ApiConfig.baseUrl}auth/login/'),
    headers: ApiConfig.headers(),
    body: json.encode({
      'username': username,
      'password': password,
    }),
  );
  
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    // Guardar token en SharedPreferences
    await saveToken(data['token']);
    return data;
  } else {
    throw Exception('Login fallido');
  }
}
```

---

### 2. Registro
**POST** `/api/auth/register/`

**Body:**
```json
{
  "username": "nuevo_cliente",
  "email": "nuevo@example.com",
  "password": "password123",
  "password2": "password123",
  "first_name": "Juan",
  "last_name": "Pérez"
}
```

**Respuesta Exitosa (201):**
```json
{
  "mensaje": "Usuario registrado exitosamente",
  "token": "abc123...",
  "usuario": {
    "id": 5,
    "username": "nuevo_cliente",
    "email": "nuevo@example.com",
    "rol": "cliente",
    "saldo": 0.00
  }
}
```

---

### 3. Logout
**POST** `/api/auth/logout/`

**Headers:** `Authorization: Token <tu_token>`

**Respuesta (200):**
```json
{
  "mensaje": "Sesión cerrada exitosamente"
}
```

---

### 4. Mi Perfil
**GET** `/api/auth/mi-perfil/`

**Headers:** `Authorization: Token <tu_token>`

**Respuesta (200):**
```json
{
  "id": 2,
  "username": "cliente",
  "email": "cliente@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "rol": "cliente",
  "saldo": 500.00,
  "date_joined": "2025-01-15T10:30:00Z"
}
```

---

## 👤 Endpoints para Clientes

### 1. Consultar Menú
**GET** `/api/cliente/menu/`

**Headers:** No requiere autenticación

**Respuesta (200):**
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
          "nombre": "Burrito de Pollo",
          "descripcion": "Burrito con pollo a la parrilla",
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
          "id": 3,
          "nombre": "Refresco",
          "descripcion": "Refresco de 500ml",
          "precio": "20.00",
          "categoria_nombre": "Bebidas"
        }
      ]
    }
  ],
  "total_categorias": 2
}
```

**Ejemplo Flutter:**
```dart
class Producto {
  final int id;
  final String nombre;
  final String descripcion;
  final double precio;
  final String categoriaNombre;

  Producto({
    required this.id,
    required this.nombre,
    required this.descripcion,
    required this.precio,
    required this.categoriaNombre,
  });

  factory Producto.fromJson(Map<String, dynamic> json) {
    return Producto(
      id: json['id'],
      nombre: json['nombre'],
      descripcion: json['descripcion'],
      precio: double.parse(json['precio']),
      categoriaNombre: json['categoria_nombre'],
    );
  }
}

Future<List<Categoria>> obtenerMenu() async {
  final response = await http.get(
    Uri.parse('${ApiConfig.baseUrl}cliente/menu/'),
  );
  
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    List<Categoria> categorias = [];
    
    for (var cat in data['categorias']) {
      categorias.add(Categoria.fromJson(cat));
    }
    
    return categorias;
  } else {
    throw Exception('Error al cargar el menú');
  }
}
```

---

### 2. Crear Pedido
**POST** `/api/pedidos/`

**Headers:** `Authorization: Token <tu_token>`

**Body:**
```json
{
  "productos": [1, 2, 3],
  "estatus": "pendiente"
}
```

**Respuesta Exitosa (201):**
```json
{
  "id": 10,
  "cliente": 2,
  "productos": [1, 2, 3],
  "total": "175.00",
  "estatus": "pendiente",
  "fecha": "2025-10-26T20:30:00Z"
}
```

**Respuesta con Saldo Insuficiente (400):**
```json
{
  "error": "Saldo insuficiente.",
  "saldo_actual": 100.00,
  "total_pedido": 175.00,
  "faltante": 75.00
}
```

**Ejemplo Flutter:**
```dart
Future<Map<String, dynamic>> crearPedido(List<int> productosIds, String token) async {
  final response = await http.post(
    Uri.parse('${ApiConfig.baseUrl}pedidos/'),
    headers: ApiConfig.headers(token: token),
    body: json.encode({
      'productos': productosIds,
      'estatus': 'pendiente',
    }),
  );
  
  if (response.statusCode == 201) {
    return json.decode(response.body);
  } else if (response.statusCode == 400) {
    final error = json.decode(response.body);
    throw Exception('${error['error']} - Faltante: \$${error['faltante']}');
  } else {
    throw Exception('Error al crear pedido');
  }
}
```

---

### 3. Consultar Mis Pedidos
**GET** `/api/cliente/mis-pedidos/`

**Parámetros de Query:**
- `?tipo=actuales` - Solo pedidos pendiente o en_proceso
- `?tipo=pasados` - Solo pedidos completado o cancelado
- `?estatus=pendiente` - Filtrar por estatus específico

**Headers:** `Authorization: Token <tu_token>`

**Respuesta (200):**
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
          "nombre": "Burrito de Carne",
          "precio": 80.00
        },
        {
          "id": 3,
          "nombre": "Refresco",
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

**Ejemplo Flutter:**
```dart
Future<List<Pedido>> obtenerMisPedidos({String? tipo, String token}) async {
  String url = '${ApiConfig.baseUrl}cliente/mis-pedidos/';
  
  if (tipo != null) {
    url += '?tipo=$tipo';
  }
  
  final response = await http.get(
    Uri.parse(url),
    headers: ApiConfig.headers(token: token),
  );
  
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    List<Pedido> pedidos = [];
    
    for (var p in data['pedidos']) {
      pedidos.add(Pedido.fromJson(p));
    }
    
    return pedidos;
  } else {
    throw Exception('Error al cargar pedidos');
  }
}
```

---

### 4. Consultar Mi Saldo
**GET** `/api/cliente/mi-saldo/`

**Headers:** `Authorization: Token <tu_token>`

**Respuesta (200):**
```json
{
  "saldo": 500.00,
  "usuario": "cliente",
  "email": "cliente@example.com",
  "fecha_consulta": "2025-10-26T18:30:00Z"
}
```

---

### 5. Recargar Saldo
**POST** `/api/cliente/recargar-saldo/`

**Headers:** `Authorization: Token <tu_token>`

**Body:**
```json
{
  "monto": 100.00
}
```

**Validaciones:**
- Monto mínimo: $0.01
- Monto máximo: $10,000.00

**Respuesta Exitosa (200):**
```json
{
  "mensaje": "Saldo recargado exitosamente",
  "monto_recargado": 100.00,
  "saldo_anterior": 500.00,
  "saldo_actual": 600.00,
  "usuario": "cliente",
  "fecha_recarga": "2025-10-26T18:35:00Z"
}
```

**Ejemplo Flutter:**
```dart
Future<Map<String, dynamic>> recargarSaldo(double monto, String token) async {
  final response = await http.post(
    Uri.parse('${ApiConfig.baseUrl}cliente/recargar-saldo/'),
    headers: ApiConfig.headers(token: token),
    body: json.encode({
      'monto': monto,
    }),
  );
  
  if (response.statusCode == 200) {
    return json.decode(response.body);
  } else {
    final error = json.decode(response.body);
    throw Exception(error['detalles']['monto'][0]);
  }
}
```

---

## 👨‍💼 Endpoints para Administradores

### 1. Listar Todos los Usuarios
**GET** `/api/usuarios/`

**Headers:** `Authorization: Token <admin_token>`

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "rol": "admin",
    "saldo": 0.00
  },
  {
    "id": 2,
    "username": "cliente",
    "email": "cliente@example.com",
    "rol": "cliente",
    "saldo": 500.00
  }
]
```

---

### 2. Listar Todos los Pedidos
**GET** `/api/pedidos/`

**Headers:** `Authorization: Token <admin_token>`

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "cliente": 2,
    "productos": [1, 2],
    "total": "155.00",
    "estatus": "pendiente",
    "fecha": "2025-10-26T18:00:00Z"
  }
]
```

---

### 3. Actualizar Estatus de Pedido
**PATCH** `/api/pedidos/{id}/`

**Headers:** `Authorization: Token <admin_token>`

**Body:**
```json
{
  "estatus": "completado"
}
```

**Respuesta (200):**
```json
{
  "id": 1,
  "cliente": 2,
  "productos": [1, 2],
  "total": "155.00",
  "estatus": "completado",
  "fecha": "2025-10-26T18:00:00Z"
}
```

---

### 4. Gestionar Productos
**GET** `/api/productos/` - Listar productos activos  
**POST** `/api/productos/` - Crear producto  
**PATCH** `/api/productos/{id}/` - Actualizar producto  
**DELETE** `/api/productos/{id}/` - Eliminar producto  

---

### 5. Gestionar Categorías
**GET** `/api/categorias/` - Listar categorías  
**POST** `/api/categorias/` - Crear categoría  
**PATCH** `/api/categorias/{id}/` - Actualizar categoría  
**DELETE** `/api/categorias/{id}/` - Eliminar categoría  

---

## 📦 Modelos de Datos

### Usuario
```dart
class Usuario {
  final int id;
  final String username;
  final String email;
  final String rol; // 'super', 'admin', 'cliente'
  final double saldo;
  final DateTime dateJoined;

  Usuario({
    required this.id,
    required this.username,
    required this.email,
    required this.rol,
    required this.saldo,
    required this.dateJoined,
  });

  factory Usuario.fromJson(Map<String, dynamic> json) {
    return Usuario(
      id: json['id'],
      username: json['username'],
      email: json['email'],
      rol: json['rol'],
      saldo: json['saldo'].toDouble(),
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
  final String categoriaNombre;

  Producto({
    required this.id,
    required this.nombre,
    required this.descripcion,
    required this.precio,
    required this.categoriaNombre,
  });

  factory Producto.fromJson(Map<String, dynamic> json) {
    return Producto(
      id: json['id'],
      nombre: json['nombre'],
      descripcion: json['descripcion'],
      precio: double.parse(json['precio'].toString()),
      categoriaNombre: json['categoria_nombre'],
    );
  }
}
```

### Pedido
```dart
class Pedido {
  final int id;
  final int clienteId;
  final String clienteNombre;
  final List<ProductoDetalle> productos;
  final double total;
  final String estatus;
  final DateTime fecha;

  Pedido({
    required this.id,
    required this.clienteId,
    required this.clienteNombre,
    required this.productos,
    required this.total,
    required this.estatus,
    required this.fecha,
  });

  factory Pedido.fromJson(Map<String, dynamic> json) {
    List<ProductoDetalle> productos = [];
    for (var p in json['productos_detalle']) {
      productos.add(ProductoDetalle.fromJson(p));
    }

    return Pedido(
      id: json['id'],
      clienteId: json['cliente'],
      clienteNombre: json['cliente_nombre'],
      productos: productos,
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
      precio: json['precio'].toDouble(),
    );
  }
}
```

---

## ⚠️ Manejo de Errores

### Códigos de Estado HTTP
- **200** - OK (Operación exitosa)
- **201** - Created (Recurso creado exitosamente)
- **400** - Bad Request (Datos inválidos o saldo insuficiente)
- **401** - Unauthorized (Token inválido o no proporcionado)
- **403** - Forbidden (Sin permisos)
- **404** - Not Found (Recurso no encontrado)
- **500** - Server Error (Error del servidor)

### Manejo de Errores en Flutter
```dart
Future<T> handleApiCall<T>(Future<http.Response> Function() apiCall) async {
  try {
    final response = await apiCall();
    
    switch (response.statusCode) {
      case 200:
      case 201:
        return json.decode(response.body);
      
      case 400:
        final error = json.decode(response.body);
        throw BadRequestException(error['error'] ?? 'Datos inválidos');
      
      case 401:
        throw UnauthorizedException('Token inválido. Por favor inicia sesión nuevamente');
      
      case 403:
        throw ForbiddenException('No tienes permisos para esta acción');
      
      case 404:
        throw NotFoundException('Recurso no encontrado');
      
      default:
        throw ServerException('Error del servidor');
    }
  } catch (e) {
    throw Exception('Error de conexión: $e');
  }
}
```

---

## 🔄 Flujo Completo de Uso

### 1. Autenticación y Configuración Inicial
```dart
// 1. Login
final loginData = await login('cliente', 'cliente123');
final token = loginData['token'];
await saveToken(token);

// 2. Obtener perfil
final perfil = await obtenerPerfil(token);
```

### 2. Consultar Menú y Crear Pedido
```dart
// 1. Obtener menú
final categorias = await obtenerMenu();

// 2. Usuario selecciona productos
List<int> productosSeleccionados = [1, 2, 3]; // IDs de productos

// 3. Verificar saldo antes de crear pedido
final saldoData = await obtenerMiSaldo(token);
double saldoActual = saldoData['saldo'];

// 4. Crear pedido
try {
  final pedido = await crearPedido(productosSeleccionados, token);
  print('Pedido creado: #${pedido['id']}');
  print('Nuevo saldo: Consultar con /cliente/mi-saldo/');
} catch (e) {
  // Manejo de saldo insuficiente
  print('Error: $e');
  // Mostrar opción de recargar saldo
}
```

### 3. Recargar Saldo
```dart
// Recargar $100
final recarga = await recargarSaldo(100.00, token);
print('Nuevo saldo: \$${recarga['saldo_actual']}');
```

### 4. Consultar Pedidos
```dart
// Obtener pedidos actuales
final pedidosActuales = await obtenerMisPedidos(tipo: 'actuales', token: token);

// Obtener pedidos pasados
final pedidosPasados = await obtenerMisPedidos(tipo: 'pasados', token: token);
```

---

## 📱 Pantallas Sugeridas para Flutter

### Para Cliente
1. **Login / Registro**
2. **Dashboard** - Resumen con saldo, pedidos recientes
3. **Menú** - Lista de categorías con productos
4. **Carrito** - Selección de productos
5. **Mis Pedidos** - Tabs para actuales/pasados
6. **Mi Saldo** - Visualización y opción de recarga
7. **Perfil** - Datos del usuario

### Para Administrador
1. **Dashboard Admin** - Estadísticas del sistema
2. **Gestión de Productos** - CRUD completo
3. **Gestión de Categorías** - CRUD completo
4. **Gestión de Pedidos** - Lista y actualización de estatus
5. **Gestión de Usuarios** - Lista de usuarios y saldos

---

## 🚀 Notas Importantes

1. **Autenticación:** Todos los endpoints protegidos requieren el header `Authorization: Token <token>`

2. **Saldos:** Al crear un pedido, el saldo se descuenta automáticamente. La API valida saldo suficiente.

3. **Productos Activos:** Solo se muestran productos con `activo=True` en el menú.

4. **Estados de Pedidos:** 
   - `pendiente` - Recién creado
   - `en_proceso` - En preparación
   - `completado` - Entregado
   - `cancelado` - Cancelado

5. **Validaciones:**
   - Monto de recarga: $0.01 - $10,000
   - Password mínimo: 6 caracteres
   - Email único por usuario

---

## 📞 Contacto

**Desarrollador:** Bernardo Prado  
**Repositorio:** https://github.com/BernardoPD/burritos-to-go-api  
**Email:** [Tu email]

---

**Última actualización:** 2025-10-26
