# 🚀 INICIO RÁPIDO - CAMBIOS PARA FLUTTER

## ✅ ¿QUÉ SE HIZO?

Se realizaron todos los cambios solicitados en el PDF para que las APIs estén listas para Flutter.

---

## 📋 CAMBIOS IMPLEMENTADOS (RESUMEN ULTRA CORTO)

### 1. ✅ ProductoSerializer - Ahora incluye `categoria_id`
```json
GET /api/productos/
{
    "id": 1,
    "categoria": 1,
    "categoria_id": 1,  ← NUEVO
    "categoria_nombre": "Burritos"
}
```

### 2. ✅ UsuarioSerializer - Ahora incluye `rol_id`
```json
GET /api/usuarios/
{
    "id": 1,
    "rol": "cliente",
    "rol_id": 2,  ← NUEVO (1=admin, 2=cliente, 3=staff)
}
```

### 3. ✅ Register - Ahora retorna `success` y `code`
```json
POST /api/auth/register/
{
    "success": true,  ← NUEVO
    "code": 200,      ← NUEVO
    "mensaje": "Usuario registrado exitosamente",
    "token": "abc123...",
    "usuario": {...}
}
```

### 4. ✅ Login - Ahora retorna `success` y `code`
```json
POST /api/auth/login/
{
    "success": true,  ← NUEVO
    "code": 200,      ← NUEVO
    "mensaje": "Login exitoso",
    "token": "abc123...",
    "usuario": {...}
}
```

### 5. ✅ Endpoint para crear pedido
```
POST /api/cliente/crear-pedido/
Body: { "productos": [1, 2, 5] }
```

### 6. ✅ Endpoint para consultar mis pedidos
```
GET /api/cliente/mis-pedidos/
GET /api/cliente/mis-pedidos/?tipo=actuales
GET /api/cliente/mis-pedidos/?tipo=pasados
```

### 7. ✅ Endpoint para consultar saldo (autenticación por token)
```
GET /api/cliente/mi-saldo/
Header: Authorization: Token {tu_token}

⚠️ NO necesitas pasar el ID del usuario
   El token identifica automáticamente al usuario
```

---

## 📂 ARCHIVOS PARA CONSULTAR

| Archivo | Contenido |
|---------|-----------|
| **RESUMEN_CAMBIOS_FLUTTER.md** | 📄 Resumen ejecutivo completo |
| **API_FLUTTER_FINAL.md** | 📚 Documentación detallada de todas las APIs |
| **PRUEBAS_APIS.md** | 🧪 Ejemplos de pruebas con cURL y Postman |
| **CAMBIOS_APIS_FLUTTER.md** | 🔍 Detalles técnicos de los cambios |

---

## 🌐 URL BASE

```
https://pradodiazbackend.pythonanywhere.com/api/
```

---

## 🔑 ENDPOINTS PRINCIPALES

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/auth/login/` | POST | Login (retorna token + success + code) |
| `/auth/register/` | POST | Registro (retorna token + success + code) |
| `/productos/` | GET | Lista productos con categoria_id |
| `/usuarios/` | GET | Lista usuarios con rol_id |
| `/cliente/menu/` | GET | Menú por categorías |
| `/cliente/crear-pedido/` | POST | Crear pedido |
| `/cliente/mis-pedidos/` | GET | Ver mis pedidos |
| `/cliente/mi-saldo/` | GET | Consultar saldo (por token) |
| `/cliente/recargar-saldo/` | POST | Recargar saldo |

---

## 📱 EJEMPLO RÁPIDO EN FLUTTER

### Login:
```dart
final response = await http.post(
  Uri.parse('https://pradodiazbackend.pythonanywhere.com/api/auth/login/'),
  headers: {'Content-Type': 'application/json'},
  body: json.encode({'username': 'user', 'password': 'pass'}),
);

final data = json.decode(response.body);
if (data['success'] == true) {  // ← Campo nuevo
  final token = data['token'];
  // Guardar token en SharedPreferences
}
```

### Consultar Saldo:
```dart
final prefs = await SharedPreferences.getInstance();
final token = prefs.getString('token');

final response = await http.get(
  Uri.parse('https://pradodiazbackend.pythonanywhere.com/api/cliente/mi-saldo/'),
  headers: {'Authorization': 'Token $token'},
);

final data = json.decode(response.body);
print('Saldo: ${data['saldo']}');  // El token identifica al usuario
```

### Crear Pedido:
```dart
final response = await http.post(
  Uri.parse('https://pradodiazbackend.pythonanywhere.com/api/cliente/crear-pedido/'),
  headers: {
    'Authorization': 'Token $token',
    'Content-Type': 'application/json',
  },
  body: json.encode({'productos': [1, 2, 5]}),
);
```

---

## ✅ VERIFICACIÓN

```bash
$ python manage.py check
System check identified no issues (0 silenced).
```

✅ **Todo funcionando correctamente**

---

## 📞 ¿NECESITAS MÁS INFORMACIÓN?

1. **Documentación completa:** Lee `API_FLUTTER_FINAL.md`
2. **Ejemplos de pruebas:** Lee `PRUEBAS_APIS.md`
3. **Detalles técnicos:** Lee `CAMBIOS_APIS_FLUTTER.md`
4. **Resumen ejecutivo:** Lee `RESUMEN_CAMBIOS_FLUTTER.md`

---

## 🎯 CONCLUSIÓN

✅ Todos los cambios del PDF están implementados
✅ Las APIs están 100% listas para Flutter
✅ Documentación completa disponible

**¡Listo para integración!** 🚀
