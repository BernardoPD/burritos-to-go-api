# 📱 API REST - Documentación Completa para Flutter

## 🔐 AUTENTICACIÓN

Todas las rutas requieren autenticación mediante Token, excepto las de registro y login.

**Header requerido:**
```
Authorization: Token {tu_token_aqui}
```

---

## 1️⃣ REGISTRO DE USUARIO

**POST** `/api/auth/register/`

### Request Body:
```json
{
    "username": "guiegar",
    "email": "guiegar@gmail.com",
    "password": "password123",
    "password2": "password123",
    "first_name": "Guillermo",
    "last_name": "Garcia"
}
```

### Response (200 OK):
```json
{
    "success": true,
    "code": 200,
    "mensaje": "Usuario registrado exitosamente",
    "token": "5f2b3fdf4f1ff094c5d879945d588328192dfcac",
    "usuario": {
        "id": 6,
        "username": "guiegar",
        "email": "guiegar@gmail.com",
        "rol": "cliente",
        "saldo": 0.0
    }
}
```

### Errores Posibles:
- 400: Datos inválidos, email duplicado, contraseñas no coinciden

---

## 2️⃣ LOGIN DE USUARIO

**POST** `/api/auth/login/`

### Request Body:
```json
{
    "username": "cliente1",
    "password": "password123"
}
```

### Response (200 OK):
```json
{
    "success": true,
    "code": 200,
    "mensaje": "Login exitoso",
    "token": "5f2b3fdf4f1ff094c5d879945d588328192dfcac",
    "usuario": {
        "id": 1,
        "username": "cliente1",
        "email": "cliente1@example.com",
        "rol": "cliente",
        "saldo": 500.0
    }
}
```

### Errores Posibles:
- 400: Credenciales inválidas, usuario inactivo

---

## 3️⃣ CERRAR SESIÓN

**POST** `/api/auth/logout/`

### Headers:
```
Authorization: Token {tu_token}
```

### Response (200 OK):
```json
{
    "mensaje": "Sesión cerrada exitosamente"
}
```

---

## 4️⃣ CONSULTAR MI PERFIL

**GET** `/api/auth/mi-perfil/`

### Headers:
```
Authorization: Token {tu_token}
```

### Response (200 OK):
```json
{
    "id": 1,
    "username": "cliente1",
    "email": "cliente1@example.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "rol": "cliente",
    "saldo": 500.0,
    "date_joined": "2025-01-15T10:30:00Z"
}
```

---

## 5️⃣ CONSULTAR MENÚ (Lista de Productos por Categoría)

**GET** `/api/cliente/menu/`

### Headers:
```
Authorization: Token {tu_token}
```

### Response (200 OK):
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
                    "id": 5,
                    "nombre": "Agua Fresca",
                    "descripcion": "Agua fresca de horchata",
                    "precio": "25.00",
                    "categoria_nombre": "Bebidas"
                }
            ]
        }
    ],
    "total_categorias": 2
}
```

---

## 6️⃣ LISTA DE PRODUCTOS (con categoria_id)

**GET** `/api/productos/`

### Headers:
```
Authorization: Token {tu_token}
```

### Response (200 OK):
```json
[
    {
        "id": 1,
        "nombre": "Burrito de Carne",
        "descripcion": "Delicioso burrito con carne asada",
        "precio": "80.00",
        "categoria": 1,
        "categoria_id": 1,
        "categoria_nombre": "Burritos",
        "activo": true
    },
    {
        "id": 2,
        "nombre": "Burrito de Pollo",
        "descripcion": "Burrito con pollo a la parrilla",
        "precio": "75.00",
        "categoria": 1,
        "categoria_id": 1,
        "categoria_nombre": "Burritos",
        "activo": true
    }
]
```

---

## 7️⃣ LISTA DE USUARIOS (con rol_id)

**GET** `/api/usuarios/`

### Headers:
```
Authorization: Token {tu_token}
```

### Response (200 OK):
```json
[
    {
        "id": 1,
        "username": "cliente1",
        "email": "cliente1@example.com",
        "rol": "cliente",
        "rol_id": 2,
        "saldo": 500.0
    },
    {
        "id": 2,
        "username": "admin",
        "email": "admin@example.com",
        "rol": "admin",
        "rol_id": 1,
        "saldo": 0.0
    }
]
```

**Mapeo de roles:**
- `admin` → `rol_id: 1`
- `cliente` → `rol_id: 2`
- `staff` → `rol_id: 3`

---

## 8️⃣ CREAR PEDIDO (Cliente)

**POST** `/api/cliente/crear-pedido/`

### Headers:
```
Authorization: Token {tu_token}
```

### Request Body:
```json
{
    "productos": [1, 2, 5]
}
```

### Response (200 OK):
```json
{
    "mensaje": "Pedido creado exitosamente.",
    "pedido_id": 10,
    "total": 180.0,
    "productos": ["Burrito de Carne", "Burrito de Pollo", "Agua Fresca"],
    "fecha": "2025-01-20T15:30:00Z",
    "saldo_restante": 320.0
}
```

### Errores Posibles:
```json
{
    "error": "Saldo insuficiente.",
    "saldo_actual": 100.0,
    "total_pedido": 180.0,
    "faltante": 80.0
}
```

---

## 9️⃣ CONSULTAR MIS PEDIDOS

**GET** `/api/cliente/mis-pedidos/`

### Headers:
```
Authorization: Token {tu_token}
```

### Parámetros opcionales:
- `?tipo=actuales` - Pedidos pendientes o en proceso
- `?tipo=pasados` - Pedidos completados o cancelados
- `?estatus=pendiente` - Filtrar por estatus específico

### Response (200 OK):
```json
{
    "pedidos": [
        {
            "id": 10,
            "cliente": 1,
            "cliente_nombre": "cliente1",
            "productos_detalle": [
                {
                    "id": 1,
                    "nombre": "Burrito de Carne",
                    "precio": 80.0
                },
                {
                    "id": 2,
                    "nombre": "Burrito de Pollo",
                    "precio": 75.0
                }
            ],
            "total": "155.00",
            "estatus": "pendiente",
            "fecha": "2025-01-20T15:30:00Z"
        }
    ],
    "total": 1,
    "filtros_aplicados": {
        "tipo": "actuales",
        "estatus": null
    }
}
```

**Estatus posibles:**
- `pendiente`
- `en_proceso`
- `completado`
- `cancelado`

---

## 🔟 CONSULTAR MI SALDO

**GET** `/api/cliente/mi-saldo/`

### Headers:
```
Authorization: Token {tu_token}
```

**⚠️ IMPORTANTE:** El endpoint usa el token para identificar al usuario automáticamente. NO necesitas pasar el ID del usuario.

### Response (200 OK):
```json
{
    "saldo": 500.0,
    "usuario": "cliente1",
    "email": "cliente1@example.com",
    "fecha_consulta": "2025-01-20T16:00:00Z"
}
```

---

## 1️⃣1️⃣ RECARGAR SALDO

**POST** `/api/cliente/recargar-saldo/`

### Headers:
```
Authorization: Token {tu_token}
```

### Request Body:
```json
{
    "monto": 100.00
}
```

### Response (200 OK):
```json
{
    "mensaje": "Saldo recargado exitosamente",
    "monto_recargado": 100.0,
    "saldo_anterior": 500.0,
    "saldo_actual": 600.0,
    "usuario": "cliente1",
    "fecha_recarga": "2025-01-20T16:15:00Z"
}
```

### Validaciones:
- Monto mínimo: $0.01
- Monto máximo: $10,000.00

### Errores Posibles:
```json
{
    "error": "Datos inválidos",
    "detalles": {
        "monto": ["El monto debe ser mayor a 0"]
    }
}
```

---

## 📋 RESUMEN DE ENDPOINTS

| Método | Endpoint | Autenticación | Descripción |
|--------|----------|---------------|-------------|
| POST | `/api/auth/register/` | ❌ No | Registrar nuevo usuario |
| POST | `/api/auth/login/` | ❌ No | Iniciar sesión |
| POST | `/api/auth/logout/` | ✅ Sí | Cerrar sesión |
| GET | `/api/auth/mi-perfil/` | ✅ Sí | Ver perfil del usuario |
| GET | `/api/cliente/menu/` | ✅ Sí | Ver menú por categorías |
| GET | `/api/productos/` | ✅ Sí | Lista de productos (con categoria_id) |
| GET | `/api/usuarios/` | ✅ Sí | Lista de usuarios (con rol_id) |
| POST | `/api/cliente/crear-pedido/` | ✅ Sí | Crear nuevo pedido |
| GET | `/api/cliente/mis-pedidos/` | ✅ Sí | Ver mis pedidos |
| GET | `/api/cliente/mi-saldo/` | ✅ Sí | Consultar mi saldo |
| POST | `/api/cliente/recargar-saldo/` | ✅ Sí | Recargar saldo |

---

## 🔧 CONFIGURACIÓN EN FLUTTER

### 1. Agregar Headers de Autenticación:

```dart
Future<http.Response> hacerPeticion(String endpoint) async {
  final token = await obtenerToken(); // Desde SharedPreferences
  
  return http.get(
    Uri.parse('https://pradodiazbackend.pythonanywhere.com/api/$endpoint'),
    headers: {
      'Authorization': 'Token $token',
      'Content-Type': 'application/json',
    },
  );
}
```

### 2. Ejemplo Login y Guardar Token:

```dart
Future<void> login(String username, String password) async {
  final response = await http.post(
    Uri.parse('https://pradodiazbackend.pythonanywhere.com/api/auth/login/'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode({
      'username': username,
      'password': password,
    }),
  );
  
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    
    if (data['success'] == true) {
      final token = data['token'];
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', token);
      await prefs.setString('username', data['usuario']['username']);
      await prefs.setDouble('saldo', data['usuario']['saldo']);
    }
  }
}
```

### 3. Ejemplo Crear Pedido:

```dart
Future<void> crearPedido(List<int> productosIds) async {
  final token = await obtenerToken();
  
  final response = await http.post(
    Uri.parse('https://pradodiazbackend.pythonanywhere.com/api/cliente/crear-pedido/'),
    headers: {
      'Authorization': 'Token $token',
      'Content-Type': 'application/json',
    },
    body: json.encode({
      'productos': productosIds,
    }),
  );
  
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    print('Pedido creado: ${data['pedido_id']}');
    print('Saldo restante: ${data['saldo_restante']}');
  }
}
```

### 4. Ejemplo Consultar Saldo:

```dart
Future<double> consultarSaldo() async {
  final token = await obtenerToken();
  
  final response = await http.get(
    Uri.parse('https://pradodiazbackend.pythonanywhere.com/api/cliente/mi-saldo/'),
    headers: {
      'Authorization': 'Token $token',
    },
  );
  
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    return data['saldo'];
  }
  
  return 0.0;
}
```

---

## ✅ CAMBIOS IMPLEMENTADOS

1. ✅ **ProductoSerializer**: Agregado `categoria_id`
2. ✅ **UsuarioSerializer**: Agregado `rol_id` (1=admin, 2=cliente, 3=staff)
3. ✅ **RegisterView**: Agregado `success: true` y `code: 200`
4. ✅ **LoginView**: Agregado `success: true` y `code: 200`
5. ✅ **Endpoint crear pedido**: Ya existente en `/api/cliente/crear-pedido/`
6. ✅ **Endpoint mis pedidos**: Ya existente en `/api/cliente/mis-pedidos/`
7. ✅ **Endpoint mi saldo**: Autenticación por token automática

---

## 🌐 URL BASE DE PRODUCCIÓN

```
https://pradodiazbackend.pythonanywhere.com/api/
```

**Ejemplo completo:**
```
https://pradodiazbackend.pythonanywhere.com/api/auth/login/
https://pradodiazbackend.pythonanywhere.com/api/cliente/menu/
https://pradodiazbackend.pythonanywhere.com/api/cliente/crear-pedido/
```

---

¡Todo listo para integración con Flutter! 🚀
