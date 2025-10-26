# 📦 PAQUETE COMPLETO PARA EQUIPO DE FRONTEND FLUTTER
## Burritos To Go API - Sistema de Pedidos

---

## 🎯 Resumen Ejecutivo

Este paquete contiene toda la información necesaria para que el equipo de **Frontend Flutter** pueda consumir la API de Burritos To Go. El sistema ya está **100% funcional** tanto en local como en producción (PythonAnywhere).

---

## ✅ ¿Qué está incluido?

### 1. **API REST Completamente Funcional**
   - ✅ Sistema de autenticación con tokens
   - ✅ Endpoints para clientes (hacer pedidos, consultar menú, gestionar saldo)
   - ✅ Endpoints para administradores (gestionar productos, categorías, pedidos)
   - ✅ Descuento automático de saldo al crear pedidos
   - ✅ Validación de saldo suficiente
   - ✅ Panel web para clientes y administradores

### 2. **Documentación Completa**
   - ✅ Todos los endpoints documentados con ejemplos
   - ✅ Modelos de datos en Dart para Flutter
   - ✅ Ejemplos de código Flutter listo para usar
   - ✅ Manejo de errores y códigos HTTP

### 3. **Deployment en PythonAnywhere**
   - ✅ API desplegada y accesible públicamente
   - ✅ Base de datos MySQL configurada
   - ✅ Datos de prueba pre-cargados

---

## 📚 Archivos a Entregar al Equipo Frontend

### 📄 1. DOCUMENTACION_COMPLETA_FRONTEND.md
**Descripción:** Documentación técnica completa de la API

**Contiene:**
- 🔑 Todos los endpoints con ejemplos de request/response
- 📦 Modelos de datos en Dart (Usuario, Producto, Pedido, etc.)
- 💻 Ejemplos de código Flutter para cada endpoint
- ⚠️ Manejo de errores y validaciones
- 🔄 Flujo completo de uso (login → hacer pedido → consultar historial)

**¿Para qué sirve?**
El equipo de frontend puede copiar/pegar los modelos Dart y los ejemplos de código directamente en su proyecto Flutter.

---

### 📄 2. GUIA_DEPLOYMENT_PYTHONANYWHERE_COMPLETA.md
**Descripción:** Guía paso a paso del deployment

**Contiene:**
- 🚀 Proceso completo de deployment en PythonAnywhere
- 🔧 Configuración de base de datos MySQL
- 📝 Script para poblar datos de prueba
- 🛠️ Solución de problemas comunes
- ✅ Checklist de verificación

**¿Para qué sirve?**
Para entender cómo está desplegada la API y poder replicarla si es necesario.

---

### 📄 3. rules.md (Actualizado)
**Descripción:** Reglas de desarrollo y arquitectura del proyecto

**Contiene:**
- 🏗️ Arquitectura del sistema
- 📊 Diagramas de modelos de datos
- 📝 Convenciones de código
- 🐛 Historial de correcciones de bugs
- ✨ Buenas prácticas aplicadas

**¿Para qué sirve?**
Para entender la lógica de negocio y las decisiones técnicas del backend.

---

## 🌐 URLs de Producción

### API Base URL
```
https://pradodiazbackend.pythonanywhere.com/api/
```

### Endpoints Principales
```dart
// Configuración en Flutter
class ApiConfig {
  static const String baseUrl = 'https://pradodiazbackend.pythonanywhere.com/api/';
  
  // Autenticación
  static const String login = '${baseUrl}auth/login/';
  static const String register = '${baseUrl}auth/register/';
  static const String logout = '${baseUrl}auth/logout/';
  
  // Cliente
  static const String menu = '${baseUrl}cliente/menu/';
  static const String misPedidos = '${baseUrl}cliente/mis-pedidos/';
  static const String miSaldo = '${baseUrl}cliente/mi-saldo/';
  static const String recargarSaldo = '${baseUrl}cliente/recargar-saldo/';
  static const String crearPedido = '${baseUrl}pedidos/';
  
  // Admin
  static const String usuarios = '${baseUrl}usuarios/';
  static const String productos = '${baseUrl}productos/';
  static const String categorias = '${baseUrl}categorias/';
  static const String pedidos = '${baseUrl}pedidos/';
}
```

---

## 🔑 Credenciales de Prueba

### Usuario Cliente
```
Username: cliente
Password: cliente123
Saldo Inicial: $500.00
```

### Usuario Administrador
```
Username: admin
Password: admin123
Permisos: Full access
```

---

## 📋 Flujo de Trabajo para Frontend

### 1. **Instalación de Dependencias en Flutter**
```yaml
# pubspec.yaml
dependencies:
  http: ^1.1.0
  shared_preferences: ^2.2.0  # Para guardar token
  provider: ^6.0.5  # Para state management (opcional)
```

---

### 2. **Implementar Autenticación**

**Ejemplo de Login:**
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<Map<String, dynamic>> login(String username, String password) async {
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
    // Guardar token
    await saveToken(data['token']);
    return data;
  } else {
    throw Exception('Login fallido');
  }
}
```

---

### 3. **Consultar Menú**

```dart
Future<List<Categoria>> obtenerMenu() async {
  final response = await http.get(
    Uri.parse('https://pradodiazbackend.pythonanywhere.com/api/cliente/menu/'),
  );
  
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    // Procesar categorías y productos
    return parseCategorias(data['categorias']);
  } else {
    throw Exception('Error al cargar menú');
  }
}
```

---

### 4. **Crear Pedido**

```dart
Future<Map<String, dynamic>> crearPedido(List<int> productosIds, String token) async {
  final response = await http.post(
    Uri.parse('https://pradodiazbackend.pythonanywhere.com/api/pedidos/'),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Token $token',
    },
    body: json.encode({
      'productos': productosIds,
      'estatus': 'pendiente',
    }),
  );
  
  if (response.statusCode == 201) {
    return json.decode(response.body);
  } else if (response.statusCode == 400) {
    // Saldo insuficiente
    final error = json.decode(response.body);
    throw SaldoInsuficienteException(error['faltante']);
  } else {
    throw Exception('Error al crear pedido');
  }
}
```

---

### 5. **Recargar Saldo**

```dart
Future<Map<String, dynamic>> recargarSaldo(double monto, String token) async {
  final response = await http.post(
    Uri.parse('https://pradodiazbackend.pythonanywhere.com/api/cliente/recargar-saldo/'),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Token $token',
    },
    body: json.encode({
      'monto': monto,
    }),
  );
  
  if (response.statusCode == 200) {
    return json.decode(response.body);
  } else {
    throw Exception('Error al recargar saldo');
  }
}
```

---

## 🎨 Pantallas Sugeridas para Flutter

### Para Cliente
1. **LoginScreen** → Login y registro
2. **HomeScreen** → Dashboard con saldo y pedidos recientes
3. **MenuScreen** → Lista de categorías y productos
4. **CarritoScreen** → Carrito de compras
5. **PedidosScreen** → Historial de pedidos (tabs: actuales/pasados)
6. **SaldoScreen** → Ver saldo y recargar
7. **PerfilScreen** → Perfil del usuario

### Para Administrador
1. **AdminDashboardScreen** → Estadísticas del sistema
2. **ProductosScreen** → CRUD de productos
3. **CategoriasScreen** → CRUD de categorías
4. **PedidosAdminScreen** → Gestión de pedidos
5. **UsuariosScreen** → Lista de usuarios

---

## 🧪 Pruebas con Postman

### Importar Colección
El repositorio incluye:
```
Burritos_API_Collection.postman_collection.json
```

**Cómo usar:**
1. Abre Postman
2. Import → Upload Files
3. Selecciona el archivo JSON
4. Prueba todos los endpoints directamente

---

## ⚠️ Puntos Importantes

### 1. **Autenticación**
Todos los endpoints protegidos requieren el header:
```
Authorization: Token <tu_token_aqui>
```

### 2. **Saldo y Pedidos**
- Al crear un pedido, el saldo se descuenta **automáticamente**
- La API valida que haya saldo suficiente antes de crear el pedido
- Si el saldo es insuficiente, retorna error 400 con el monto faltante

### 3. **Productos Activos**
- Solo se muestran productos con `activo=True`
- Los productos inactivos no aparecen en el menú

### 4. **Estados de Pedidos**
```
pendiente → en_proceso → completado
                      ↘ cancelado
```

### 5. **Validaciones**
- Password mínimo: 6 caracteres
- Monto de recarga: $0.01 - $10,000.00
- Email único por usuario

---

## 📞 Soporte y Contacto

### Información del Proyecto
- **Repositorio GitHub:** https://github.com/BernardoPD/burritos-to-go-api
- **API Producción:** https://pradodiazbackend.pythonanywhere.com/api/
- **Admin Panel:** https://pradodiazbackend.pythonanywhere.com/admin/

### Credenciales PythonAnywhere
- **Usuario:** pradodiazbackend
- **URL:** https://www.pythonanywhere.com/user/pradodiazbackend/

---

## ✅ Checklist para el Equipo Frontend

- [ ] Revisar DOCUMENTACION_COMPLETA_FRONTEND.md
- [ ] Copiar modelos Dart al proyecto Flutter
- [ ] Configurar ApiConfig con base URL de producción
- [ ] Probar endpoints con Postman
- [ ] Implementar login y guardar token
- [ ] Implementar consulta de menú
- [ ] Implementar creación de pedidos
- [ ] Implementar consulta de pedidos
- [ ] Implementar recarga de saldo
- [ ] Manejar errores (saldo insuficiente, token inválido, etc.)
- [ ] Probar flujo completo:
  - [ ] Login
  - [ ] Ver menú
  - [ ] Agregar productos al carrito
  - [ ] Crear pedido
  - [ ] Ver pedidos creados
  - [ ] Recargar saldo
  - [ ] Logout

---

## 🚀 ¿Listo para Empezar?

El equipo de frontend tiene todo lo necesario para:
1. ✅ Consumir la API desde Flutter
2. ✅ Implementar todas las funcionalidades de cliente
3. ✅ Implementar funcionalidades de administrador
4. ✅ Manejar autenticación y estado de usuario
5. ✅ Probar con datos reales en producción

---

## 📦 Resumen de Archivos

```
📁 burritos-to-go-api/
│
├── 📄 DOCUMENTACION_COMPLETA_FRONTEND.md  ← PRINCIPAL para Frontend
├── 📄 GUIA_DEPLOYMENT_PYTHONANYWHERE_COMPLETA.md
├── 📄 rules.md
├── 📄 Burritos_API_Collection.postman_collection.json
├── 📄 requirements.txt
├── 📄 README.md
│
├── 📁 core/                 ← Código del backend
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
│
└── 📁 burritos_project/     ← Configuración Django
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

---

## 🎓 Ejemplo de Clase Service en Flutter

```dart
// lib/services/api_service.dart
class ApiService {
  static const String baseUrl = 'https://pradodiazbackend.pythonanywhere.com/api/';
  
  // Login
  Future<LoginResponse> login(String username, String password) async {
    // ... implementación
  }
  
  // Menú
  Future<List<Categoria>> obtenerMenu() async {
    // ... implementación
  }
  
  // Pedidos
  Future<Pedido> crearPedido(List<int> productosIds) async {
    // ... implementación
  }
  
  Future<List<Pedido>> obtenerMisPedidos({String? tipo}) async {
    // ... implementación
  }
  
  // Saldo
  Future<SaldoResponse> obtenerMiSaldo() async {
    // ... implementación
  }
  
  Future<RecargaResponse> recargarSaldo(double monto) async {
    // ... implementación
  }
}
```

---

**Última Actualización:** 2025-10-26  
**Versión API:** 1.0  
**Estado:** ✅ Producción

---

## 💡 Notas Finales

1. La API está **100% funcional** y probada
2. Todos los endpoints retornan JSON bien estructurado
3. Los errores incluyen mensajes descriptivos
4. La documentación incluye ejemplos en Dart listos para usar
5. Los datos de prueba ya están cargados en producción

**¡El equipo de frontend puede empezar a desarrollar inmediatamente!** 🚀

---

**Desarrollado por:** Bernardo Prado  
**Framework:** Django 5.2 + Django REST Framework  
**Base de Datos:** MySQL  
**Hosting:** PythonAnywhere
