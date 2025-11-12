# 🧪 PRUEBAS DE APIS - Guía Rápida

## 📍 URL BASE
```
https://pradodiazbackend.pythonanywhere.com/api/
```

---

## 1️⃣ REGISTRO DE USUARIO

**POST** `/api/auth/register/`

### cURL:
```bash
curl -X POST https://pradodiazbackend.pythonanywhere.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "password2": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Respuesta esperada:
```json
{
    "success": true,
    "code": 200,
    "mensaje": "Usuario registrado exitosamente",
    "token": "abc123def456...",
    "usuario": {
        "id": 10,
        "username": "testuser",
        "email": "test@example.com",
        "rol": "cliente",
        "saldo": 0.0
    }
}
```

---

## 2️⃣ LOGIN

**POST** `/api/auth/login/`

### cURL:
```bash
curl -X POST https://pradodiazbackend.pythonanywhere.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "cliente1",
    "password": "password123"
  }'
```

### Respuesta esperada:
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

**⚠️ GUARDAR EL TOKEN para las siguientes peticiones**

---

## 3️⃣ CONSULTAR PRODUCTOS (con categoria_id)

**GET** `/api/productos/`

### cURL:
```bash
curl -X GET https://pradodiazbackend.pythonanywhere.com/api/productos/ \
  -H "Authorization: Token TU_TOKEN_AQUI"
```

### Respuesta esperada:
```json
[
    {
        "id": 1,
        "nombre": "Burrito de Carne",
        "descripcion": "Delicioso burrito con carne asada",
        "precio": "80.00",
        "categoria": 1,
        "categoria_id": 1,  ← NUEVO
        "categoria_nombre": "Burritos",
        "activo": true
    },
    {
        "id": 2,
        "nombre": "Burrito de Pollo",
        "descripcion": "Burrito con pollo a la parrilla",
        "precio": "75.00",
        "categoria": 1,
        "categoria_id": 1,  ← NUEVO
        "categoria_nombre": "Burritos",
        "activo": true
    }
]
```

---

## 4️⃣ CONSULTAR USUARIOS (con rol_id)

**GET** `/api/usuarios/`

### cURL:
```bash
curl -X GET https://pradodiazbackend.pythonanywhere.com/api/usuarios/ \
  -H "Authorization: Token TU_TOKEN_AQUI"
```

### Respuesta esperada:
```json
[
    {
        "id": 1,
        "username": "cliente1",
        "email": "cliente1@example.com",
        "rol": "cliente",
        "rol_id": 2,  ← NUEVO (1=admin, 2=cliente, 3=staff)
        "saldo": 500.0
    },
    {
        "id": 2,
        "username": "admin",
        "email": "admin@example.com",
        "rol": "admin",
        "rol_id": 1,  ← NUEVO
        "saldo": 0.0
    }
]
```

---

## 5️⃣ CONSULTAR MENÚ

**GET** `/api/cliente/menu/`

### cURL:
```bash
curl -X GET https://pradodiazbackend.pythonanywhere.com/api/cliente/menu/ \
  -H "Authorization: Token TU_TOKEN_AQUI"
```

### Respuesta esperada:
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
                }
            ]
        },
        {
            "id": 2,
            "nombre": "Bebidas",
            "productos": [...]
        }
    ],
    "total_categorias": 2
}
```

---

## 6️⃣ CREAR PEDIDO

**POST** `/api/cliente/crear-pedido/`

### cURL:
```bash
curl -X POST https://pradodiazbackend.pythonanywhere.com/api/cliente/crear-pedido/ \
  -H "Authorization: Token TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "productos": [1, 2, 5]
  }'
```

### Respuesta esperada:
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

### Error - Saldo insuficiente:
```json
{
    "error": "Saldo insuficiente.",
    "saldo_actual": 100.0,
    "total_pedido": 180.0,
    "faltante": 80.0
}
```

---

## 7️⃣ CONSULTAR MIS PEDIDOS

**GET** `/api/cliente/mis-pedidos/`

### cURL (todos los pedidos):
```bash
curl -X GET https://pradodiazbackend.pythonanywhere.com/api/cliente/mis-pedidos/ \
  -H "Authorization: Token TU_TOKEN_AQUI"
```

### cURL (solo pedidos actuales):
```bash
curl -X GET "https://pradodiazbackend.pythonanywhere.com/api/cliente/mis-pedidos/?tipo=actuales" \
  -H "Authorization: Token TU_TOKEN_AQUI"
```

### cURL (solo pedidos pasados):
```bash
curl -X GET "https://pradodiazbackend.pythonanywhere.com/api/cliente/mis-pedidos/?tipo=pasados" \
  -H "Authorization: Token TU_TOKEN_AQUI"
```

### Respuesta esperada:
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

---

## 8️⃣ CONSULTAR SALDO

**GET** `/api/cliente/mi-saldo/`

### cURL:
```bash
curl -X GET https://pradodiazbackend.pythonanywhere.com/api/cliente/mi-saldo/ \
  -H "Authorization: Token TU_TOKEN_AQUI"
```

### Respuesta esperada:
```json
{
    "saldo": 500.0,
    "usuario": "cliente1",
    "email": "cliente1@example.com",
    "fecha_consulta": "2025-01-20T16:00:00Z"
}
```

**⚠️ NOTA:** No necesitas pasar el ID del usuario. El token identifica automáticamente al usuario.

---

## 9️⃣ RECARGAR SALDO

**POST** `/api/cliente/recargar-saldo/`

### cURL:
```bash
curl -X POST https://pradodiazbackend.pythonanywhere.com/api/cliente/recargar-saldo/ \
  -H "Authorization: Token TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "monto": 100.00
  }'
```

### Respuesta esperada:
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

---

## 🔟 CERRAR SESIÓN

**POST** `/api/auth/logout/`

### cURL:
```bash
curl -X POST https://pradodiazbackend.pythonanywhere.com/api/auth/logout/ \
  -H "Authorization: Token TU_TOKEN_AQUI"
```

### Respuesta esperada:
```json
{
    "mensaje": "Sesión cerrada exitosamente"
}
```

---

## 📊 FLUJO COMPLETO DE PRUEBA

### 1. Registrar usuario
```bash
curl -X POST https://pradodiazbackend.pythonanywhere.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test1", "email": "test1@mail.com", "password": "pass123", "password2": "pass123", "first_name": "Test", "last_name": "One"}'
```

### 2. Hacer login (guardar token)
```bash
curl -X POST https://pradodiazbackend.pythonanywhere.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test1", "password": "pass123"}'
```

### 3. Recargar saldo
```bash
curl -X POST https://pradodiazbackend.pythonanywhere.com/api/cliente/recargar-saldo/ \
  -H "Authorization: Token TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"monto": 500.00}'
```

### 4. Ver menú
```bash
curl -X GET https://pradodiazbackend.pythonanywhere.com/api/cliente/menu/ \
  -H "Authorization: Token TU_TOKEN"
```

### 5. Crear pedido
```bash
curl -X POST https://pradodiazbackend.pythonanywhere.com/api/cliente/crear-pedido/ \
  -H "Authorization: Token TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productos": [1, 2]}'
```

### 6. Ver mis pedidos
```bash
curl -X GET https://pradodiazbackend.pythonanywhere.com/api/cliente/mis-pedidos/ \
  -H "Authorization: Token TU_TOKEN"
```

### 7. Ver mi saldo actualizado
```bash
curl -X GET https://pradodiazbackend.pythonanywhere.com/api/cliente/mi-saldo/ \
  -H "Authorization: Token TU_TOKEN"
```

---

## 🧪 PRUEBAS EN POSTMAN

### Configurar Variable de Entorno:
1. Crear colección "Burritos API"
2. Agregar variable `base_url` = `https://pradodiazbackend.pythonanywhere.com/api`
3. Agregar variable `token` (se llenará después del login)

### Request de Login:
- **URL:** `{{base_url}}/auth/login/`
- **Method:** POST
- **Body (JSON):**
```json
{
    "username": "cliente1",
    "password": "password123"
}
```
- **Tests (Script):**
```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.token);
    pm.environment.set("username", jsonData.usuario.username);
    pm.environment.set("saldo", jsonData.usuario.saldo);
}
```

### Request con Autenticación:
- **Headers:**
  - Key: `Authorization`
  - Value: `Token {{token}}`

---

## ✅ CAMBIOS VERIFICADOS

| Cambio | Estado | Verificación |
|--------|--------|--------------|
| categoria_id en productos | ✅ | Campo agregado en ProductoSerializer |
| rol_id en usuarios | ✅ | Campo agregado en UsuarioSerializer |
| success y code en register | ✅ | Response actualizado |
| success y code en login | ✅ | Response actualizado |
| Endpoint crear pedido | ✅ | Ya existía en /api/cliente/crear-pedido/ |
| Endpoint mis pedidos | ✅ | Ya existía en /api/cliente/mis-pedidos/ |
| Endpoint mi saldo | ✅ | Autenticación por token automática |

---

¡Todo listo para integración con Flutter! 🚀
