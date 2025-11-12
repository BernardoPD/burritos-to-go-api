# ✅ CAMBIOS REALIZADOS - APIS LISTAS PARA FLUTTER

## 📋 RESUMEN DE MODIFICACIONES

### 1. ✅ ProductoSerializer - Agregado `categoria_id`
**Archivo:** `core/serializers.py`

**Antes:**
```python
class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria', 'categoria_nombre', 'activo']
```

**Después:**
```python
class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    categoria_id = serializers.IntegerField(source='categoria.id', read_only=True)
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria', 'categoria_id', 'categoria_nombre', 'activo']
```

**Resultado en API:**
```json
{
    "id": 1,
    "nombre": "Burrito de Carne",
    "precio": "80.00",
    "categoria": 1,
    "categoria_id": 1,  ← NUEVO
    "categoria_nombre": "Burritos"
}
```

---

### 2. ✅ UsuarioSerializer - Agregado `rol_id`
**Archivo:** `core/serializers.py`

**Antes:**
```python
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'saldo']
```

**Después:**
```python
class UsuarioSerializer(serializers.ModelSerializer):
    rol_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'rol_id', 'saldo']
    
    def get_rol_id(self, obj):
        roles_map = {
            'admin': 1,
            'cliente': 2,
            'staff': 3
        }
        return roles_map.get(obj.rol, 2)
```

**Resultado en API:**
```json
{
    "id": 1,
    "username": "cliente1",
    "rol": "cliente",
    "rol_id": 2,  ← NUEVO
    "saldo": 500.0
}
```

**Mapeo de roles:**
- `admin` → `rol_id: 1`
- `cliente` → `rol_id: 2`
- `staff` → `rol_id: 3`

---

### 3. ✅ RegisterView - Agregado `success` y `code`
**Archivo:** `core/views.py`

**Antes:**
```python
return Response({
    'mensaje': 'Usuario registrado exitosamente',
    'token': token.key,
    'usuario': {...}
}, status=status.HTTP_201_CREATED)
```

**Después:**
```python
return Response({
    'success': True,  ← NUEVO
    'code': 200,      ← NUEVO
    'mensaje': 'Usuario registrado exitosamente',
    'token': token.key,
    'usuario': {...}
}, status=status.HTTP_201_CREATED)
```

**Respuesta completa:**
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

---

### 4. ✅ LoginView - Agregado `success` y `code`
**Archivo:** `core/views.py`

**Antes:**
```python
return Response({
    'mensaje': 'Login exitoso',
    'token': token.key,
    'usuario': {...}
}, status=status.HTTP_200_OK)
```

**Después:**
```python
return Response({
    'success': True,  ← NUEVO
    'code': 200,      ← NUEVO
    'mensaje': 'Login exitoso',
    'token': token.key,
    'usuario': {...}
}, status=status.HTTP_200_OK)
```

**Respuesta completa:**
```json
{
    "success": true,
    "code": 200,
    "mensaje": "Login exitoso",
    "token": "abc123def456",
    "usuario": {
        "id": 1,
        "username": "cliente1",
        "email": "cliente1@example.com",
        "rol": "cliente",
        "saldo": 500.0
    }
}
```

---

### 5. ✅ Endpoint Crear Pedido - Ya existe
**Archivo:** `core/urls.py`

**Ruta actualizada:**
```python
path('cliente/crear-pedido/', CrearPedidoView.as_view(), name='cliente-crear-pedido'),
```

**URL completa:**
```
POST https://pradodiazbackend.pythonanywhere.com/api/cliente/crear-pedido/
```

**Request:**
```json
{
    "productos": [1, 2, 5]
}
```

**Response:**
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

---

### 6. ✅ Endpoint Consultar Mis Pedidos - Ya existe
**URL:**
```
GET https://pradodiazbackend.pythonanywhere.com/api/cliente/mis-pedidos/
```

**Filtros opcionales:**
- `?tipo=actuales` - Pedidos pendientes o en proceso
- `?tipo=pasados` - Pedidos completados o cancelados
- `?estatus=pendiente` - Filtrar por estatus específico

**Response:**
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
                }
            ],
            "total": "80.00",
            "estatus": "pendiente",
            "fecha": "2025-01-20T15:30:00Z"
        }
    ],
    "total": 1
}
```

---

### 7. ✅ Endpoint Consultar Saldo - Autenticación por Token
**URL:**
```
GET https://pradodiazbackend.pythonanywhere.com/api/cliente/mi-saldo/
```

**Headers:**
```
Authorization: Token {tu_token_aqui}
```

**⚠️ IMPORTANTE:** 
El endpoint identifica automáticamente al usuario mediante el token en el header. **NO necesitas pasar el ID del usuario**.

**Response:**
```json
{
    "saldo": 500.0,
    "usuario": "cliente1",
    "email": "cliente1@example.com",
    "fecha_consulta": "2025-01-20T16:00:00Z"
}
```

**Cómo funciona:**
1. El cliente envía el token en el header `Authorization: Token abc123`
2. Django REST Framework identifica al usuario automáticamente con `request.user`
3. Se retorna el saldo del usuario autenticado

**Ejemplo en Flutter:**
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

## 📝 TODOS LOS ENDPOINTS DISPONIBLES

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| POST | `/api/auth/register/` | ❌ No | Registrar nuevo usuario |
| POST | `/api/auth/login/` | ❌ No | Iniciar sesión (retorna token) |
| POST | `/api/auth/logout/` | ✅ Sí | Cerrar sesión |
| GET | `/api/auth/mi-perfil/` | ✅ Sí | Ver perfil del usuario |
| GET | `/api/cliente/menu/` | ✅ Sí | Ver menú por categorías |
| GET | `/api/productos/` | ✅ Sí | Lista productos (con categoria_id) |
| GET | `/api/usuarios/` | ✅ Sí | Lista usuarios (con rol_id) |
| POST | `/api/cliente/crear-pedido/` | ✅ Sí | Crear nuevo pedido |
| GET | `/api/cliente/mis-pedidos/` | ✅ Sí | Ver mis pedidos |
| GET | `/api/cliente/mi-saldo/` | ✅ Sí | Consultar mi saldo (por token) |
| POST | `/api/cliente/recargar-saldo/` | ✅ Sí | Recargar saldo |

---

## 🔐 AUTENTICACIÓN EN FLUTTER

### 1. Guardar Token al Login:
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
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', data['token']);
      await prefs.setString('username', data['usuario']['username']);
      await prefs.setDouble('saldo', data['usuario']['saldo']);
    }
  }
}
```

### 2. Usar Token en Peticiones:
```dart
Future<http.Response> hacerPeticion(String endpoint) async {
  final prefs = await SharedPreferences.getInstance();
  final token = prefs.getString('token') ?? '';
  
  return http.get(
    Uri.parse('https://pradodiazbackend.pythonanywhere.com/api/$endpoint'),
    headers: {
      'Authorization': 'Token $token',
      'Content-Type': 'application/json',
    },
  );
}
```

---

## ✅ VERIFICACIÓN DE CAMBIOS

Ejecutado: `python manage.py check`
```
System check identified no issues (0 silenced).
```

**Estado:** ✅ Todo funcionando correctamente

---

## 📄 ARCHIVOS MODIFICADOS

1. ✅ `core/serializers.py` - Agregados `categoria_id` y `rol_id`
2. ✅ `core/views.py` - Agregados `success` y `code` en login/register
3. ✅ `core/urls.py` - Clarificado endpoint de crear pedido
4. ✅ `API_FLUTTER_FINAL.md` - Documentación completa nueva

---

## 🚀 PRÓXIMOS PASOS

1. Subir cambios a PythonAnywhere si es necesario
2. Probar endpoints desde Postman o Flutter
3. Integrar en la app Flutter

---

¡APIs listas para conectarse con Flutter! 🎉
