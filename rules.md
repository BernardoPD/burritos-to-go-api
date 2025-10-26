# 🌯 Burritos To Go - Reglas de Desarrollo y Arquitectura

## 📋 Tabla de Contenidos
1. [Información General del Proyecto](#información-general-del-proyecto)
2. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
3. [Diagrama de Arquitectura](#diagrama-de-arquitectura)
4. [Modelos de Datos](#modelos-de-datos)
5. [Reglas de Programación](#reglas-de-programación)
6. [Estructura de Directorios](#estructura-de-directorios)
7. [Convenciones de Código](#convenciones-de-código)
8. [Buenas Prácticas](#buenas-prácticas)

---

## 📌 Información General del Proyecto

**Nombre:** Burritos To Go  
**Framework:** Django 5.2.7  
**API:** Django REST Framework  
**Base de Datos:** MySQL (burritos_db)  
**Tipo:** API REST para sistema de pedidos de comida

### Propósito
Sistema de gestión de pedidos de burritos que permite:
- Gestión de usuarios con roles (Super Usuario, Administrador, Cliente)
- Catálogo de productos y categorías
- Sistema de pedidos con validación de saldo
- Administración personalizada de pedidos

---

## 🏗️ Arquitectura del Proyecto

### Patrón Arquitectónico
**MTV (Model-Template-View)** de Django con REST API

### Componentes Principales

1. **Models (Modelos)** - `core/models.py`
   - Definen la estructura de datos
   - Lógica de negocio básica
   - Relaciones entre entidades

2. **Views (Vistas)** - `core/views.py`
   - ViewSets de Django REST Framework
   - APIView personalizada para pedidos
   - Lógica de control y validaciones

3. **Serializers (Serializadores)** - `core/serializers.py`
   - Conversión de modelos a JSON
   - Validación de datos de entrada
   - Definición de campos expuestos en API

4. **URLs (Rutas)** - `core/urls.py` y `burritos_project/urls.py`
   - Enrutamiento de endpoints
   - Configuración de routers REST

5. **Admin (Administración)** - `core/admin.py`
   - Interfaz administrativa personalizada
   - Validaciones personalizadas en formularios
   - Gestión de relaciones ManyToMany

---

## 📊 Diagrama de Arquitectura

```mermaid
graph TB
    subgraph "Cliente"
        CLIENT[Cliente HTTP/API]
    end

    subgraph "Django Application"
        URLS[URLs Router<br/>burritos_project/urls.py]
        CORE_URLS[Core URLs<br/>core/urls.py]
        
        subgraph "Views Layer"
            UV[UsuarioViewSet]
            PV[ProductoViewSet]
            CV[CategoriaViewSet]
            PDV[PedidoViewSet]
            CPV[CrearPedidoView<br/>APIView]
        end
        
        subgraph "Serializers Layer"
            US[UsuarioSerializer]
            PS[ProductoSerializer]
            CS[CategoriaSerializer]
            PDS[PedidoSerializer]
            CPS[CrearPedidoSerializer]
        end
        
        subgraph "Models Layer"
            UM[Usuario<br/>AbstractUser]
            PM[Producto]
            CM[Categoria]
            PDM[Pedido]
        end
        
        subgraph "Admin Interface"
            ADMIN[Django Admin]
            PFORM[PedidoForm]
            PADMIN[PedidoAdmin]
        end
    end
    
    subgraph "Database"
        DB[(MySQL<br/>burritos_db)]
    end
    
    CLIENT -->|HTTP Request| URLS
    URLS -->|/api/| CORE_URLS
    CORE_URLS --> UV
    CORE_URLS --> PV
    CORE_URLS --> CV
    CORE_URLS --> PDV
    CORE_URLS --> CPV
    
    UV --> US --> UM
    PV --> PS --> PM
    CV --> CS --> CM
    PDV --> PDS --> PDM
    CPV --> CPS --> PDM
    
    ADMIN --> PFORM --> PADMIN --> PDM
    
    UM --> DB
    PM --> DB
    CM --> DB
    PDM --> DB
    
    style CLIENT fill:#e1f5ff
    style DB fill:#ffe1e1
    style ADMIN fill:#fff4e1
```

---

## 📦 Modelos de Datos

```mermaid
erDiagram
    Usuario ||--o{ Pedido : realiza
    Producto }o--|| Categoria : pertenece
    Pedido }o--o{ Producto : contiene
    
    Usuario {
        int id PK
        string username
        string email
        string password
        string rol
        decimal saldo
        datetime date_joined
    }
    
    Categoria {
        int id PK
        string nombre
    }
    
    Producto {
        int id PK
        string nombre
        text descripcion
        decimal precio
        int categoria_id FK
        boolean activo
    }
    
    Pedido {
        int id PK
        int cliente_id FK
        decimal total
        string estatus
        datetime fecha
    }
```

### Descripción de Modelos

#### 1. **Usuario** (Extiende AbstractUser)
- **Rol:** Define permisos (super, admin, cliente)
- **Saldo:** Billetera virtual del usuario
- **Relaciones:** Un usuario puede tener muchos pedidos
- **Custom User Model:** Configurado en `settings.AUTH_USER_MODEL = 'core.Usuario'`

#### 2. **Categoria**
- Clasificación de productos
- Relación: Una categoría tiene muchos productos

#### 3. **Producto**
- **Campo activo:** Soft delete para no eliminar productos
- **Precio:** DecimalField para precisión monetaria
- **Relación:** Pertenece a una categoría

#### 4. **Pedido**
- **ManyToMany con Productos:** Un pedido puede tener múltiples productos
- **Total:** Se calcula automáticamente en el método `save()`
- **Estatus:** Control del estado del pedido
- **Validación:** Se verifica saldo suficiente antes de crear

---

## ⚙️ Reglas de Programación

### 1. **Modelos (Models)**

#### ✅ HACER:
- Usar `DecimalField` para valores monetarios (precio, saldo, total)
  ```python
  precio = models.DecimalField(max_digits=10, decimal_places=2)
  ```
- Implementar `__str__()` en todos los modelos para representación legible
- Usar `auto_now_add=True` para timestamps de creación
- Implementar soft delete con campo `activo` en lugar de eliminar registros
- Validar lógica de negocio en el método `save()` cuando sea apropiado

#### ❌ NO HACER:
- No usar `FloatField` para dinero (impreciso)
- No eliminar físicamente registros que afecten historial
- No poner lógica de negocio compleja en modelos (usar services/views)

### 2. **Serializadores (Serializers)**

#### ✅ HACER:
- Especificar campos explícitamente cuando sea posible
  ```python
  fields = ['id', 'username', 'email', 'rol', 'saldo']
  ```
- Usar `read_only=True` para campos calculados o autogenerados
  ```python
  extra_kwargs = {
      'cliente': {'read_only': True},
      'total': {'read_only': True}
  }
  ```
- Implementar validaciones personalizadas en `validate_<field_name>()`
- Crear serializadores específicos para operaciones complejas (ej: CrearPedidoSerializer)

#### ❌ NO HACER:
- No exponer campos sensibles (passwords, tokens)
- No usar `fields = '__all__'` en producción sin revisar qué campos se exponen
- No incluir lógica de negocio en serializadores (solo validación de formato)

### 3. **Vistas (Views)**

#### ✅ HACER:
- Usar `ViewSet` para operaciones CRUD estándar
- Usar `APIView` para lógica personalizada compleja
- Filtrar querysets según contexto:
  ```python
  queryset = Producto.objects.filter(activo=True)
  ```
- Validar permisos con `permission_classes`
- Manejar errores con Response y status codes apropiados:
  ```python
  return Response({'error': 'mensaje'}, status=400)
  ```
- Usar `perform_create()` para lógica adicional en creación
- Calcular totales antes de guardar
- Validar saldo suficiente antes de procesar pedidos

#### ❌ NO HACER:
- No exponer endpoints sin validación de permisos
- No devolver errores genéricos sin contexto
- No modificar datos sin validación previa
- No confiar en datos del cliente sin sanitizar

### 4. **URLs**

#### ✅ HACER:
- Usar `DefaultRouter` para ViewSets
- Prefijos descriptivos (`api/`, versiones futuras: `api/v1/`)
- Nombres descriptivos para rutas personalizadas:
  ```python
  path('crear_pedido/', CrearPedidoView.as_view(), name='crear_pedido')
  ```
- Separar URLs por app (`core/urls.py`)

#### ❌ NO HACER:
- No mezclar URLs de diferentes apps en un solo archivo
- No usar rutas ambiguas o confusas

### 5. **Administración (Admin)**

#### ✅ HACER:
- Personalizar formularios para validaciones complejas
- Usar `filter_horizontal` para relaciones ManyToMany
- Implementar validaciones en `clean()` del formulario
- Mostrar mensajes de éxito/error al usuario:
  ```python
  messages.success(request, "✅ Operación exitosa")
  ```
- Excluir campos autocalculados del formulario:
  ```python
  exclude = ('total',)
  ```
- Pasar `request` al formulario cuando se necesite contexto

#### ❌ NO HACER:
- No permitir edición de campos calculados
- No ignorar validaciones de negocio en admin
- No exponer operaciones peligrosas sin confirmación

### 6. **Configuración (Settings)**

#### ✅ HACER:
- Mantener `SECRET_KEY` segura (usar variables de entorno en producción)
- Configurar `DEBUG = False` en producción
- Especificar `ALLOWED_HOSTS` en producción
- Registrar apps propias en `INSTALLED_APPS`
- Configurar correctamente la base de datos
- Definir `AUTH_USER_MODEL` si se usa modelo personalizado

#### ❌ NO HACER:
- No commitear `SECRET_KEY` en repositorios públicos
- No dejar `DEBUG = True` en producción
- No usar contraseñas vacías en producción

---

## 📁 Estructura de Directorios

```
burritos_to_go/
│
├── burritos_project/          # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py           # ⚙️ Configuración global
│   ├── urls.py               # 🔗 URLs principales
│   ├── asgi.py               # ASGI para deployment
│   └── wsgi.py               # WSGI para deployment
│
├── core/                      # App principal
│   ├── migrations/           # Migraciones de base de datos
│   ├── __init__.py
│   ├── admin.py              # 🛠️ Configuración admin personalizada
│   ├── apps.py               # Configuración de la app
│   ├── models.py             # 📊 Modelos de datos
│   ├── serializers.py        # 🔄 Serializadores REST
│   ├── views.py              # 👁️ Vistas y lógica de negocio
│   ├── urls.py               # 🔗 URLs de la app
│   └── tests.py              # 🧪 Tests (pendiente implementar)
│
├── venv/                      # Entorno virtual (no versionar)
├── env/                       # Entorno virtual alternativo
├── manage.py                  # 🎮 CLI de Django
└── rules.md                   # 📖 Este archivo
```

---

## 💻 Convenciones de Código

### Nomenclatura

#### Archivos y Módulos
- `snake_case` para archivos Python: `models.py`, `serializers.py`
- Nombres descriptivos: `crear_pedido_view.py`

#### Clases
- `PascalCase` para clases:
  ```python
  class UsuarioViewSet(viewsets.ModelViewSet):
  class CrearPedidoSerializer(serializers.Serializer):
  ```

#### Variables y Funciones
- `snake_case` para variables y funciones:
  ```python
  total_pedido = sum(precios)
  def calcular_total():
  ```

#### Constantes
- `UPPER_SNAKE_CASE` para constantes:
  ```python
  ROLES = (
      ('super', 'Súper Usuario'),
      ('admin', 'Administrador'),
  )
  ```

### Comentarios

#### En Español
- Comentarios informativos en español
- Emojis opcionales para mejor legibilidad:
  ```python
  # ✅ Validar saldo del cliente
  # 👈 Esta línea debe estar
  ```

#### Docstrings
- Usar docstrings para funciones y clases complejas:
  ```python
  """
  Crea un pedido validando saldo del cliente.
  
  Args:
      request: Request con productos_ids
      
  Returns:
      Response con detalles del pedido o error
  """
  ```

#### 🆕 Comentarios Descriptivos para Correcciones de Bugs

**NUEVA REGLA**: Cuando se corrige un bug o se modifica lógica crítica de negocio, agregar comentarios estructurados que documenten:

1. **PROBLEMA DETECTADO**: Descripción clara del bug
2. **CÓDIGO ANTERIOR**: Snippet del código problemático
3. **PROBLEMA**: Lista numerada de los issues específicos
4. **SOLUCIÓN IMPLEMENTADA**: Lista numerada de los cambios
5. **JUSTIFICACIÓN**: Por qué esta solución es correcta

##### ✅ FORMATO ESTÁNDAR:

```python
def metodo_corregido(self):
    """
    PROBLEMA DETECTADO: [Descripción breve del bug]
    
    CÓDIGO ANTERIOR:
        [código antiguo que causaba el problema]
    
    PROBLEMA: 
        1. [Issue específico #1]
        2. [Issue específico #2]
        3. [Issue específico #3]
    
    SOLUCIÓN IMPLEMENTADA:
        1. [Cambio realizado #1]
        2. [Cambio realizado #2]
        3. [Cambio realizado #3]
    
    JUSTIFICACIÓN:
        - [Razón por la que esta solución es correcta]
        - [Cómo previene el problema original]
        - [Qué reglas de negocio cumple]
    """
    # ✅ Código corregido con comentarios inline
    variable = valor  # Explicación de esta línea específica
```

##### 📋 EJEMPLO REAL (Bug de Saldo en Pedidos):

```python
def perform_create(self, serializer):
    """
    PROBLEMA DETECTADO: No se descontaba el saldo del cliente al crear pedido
    
    CÓDIGO ANTERIOR:
        serializer.save(cliente=self.request.user)
        productos = serializer.validated_data.get('productos', [])
        total = sum([p.precio for p in productos])
        serializer.save(cliente=self.request.user, total=total)
    
    PROBLEMA: 
        1. Se guardaba dos veces el pedido (doble save())
        2. NO se validaba saldo suficiente del cliente
        3. NO se descontaba el total del saldo del cliente
        4. Inconsistencia con otras vistas que SÍ descuentan
    
    SOLUCIÓN IMPLEMENTADA:
        1. Calcular total ANTES de guardar
        2. Validar saldo suficiente del cliente
        3. Guardar pedido UNA SOLA VEZ con todos los datos
        4. Descontar total del saldo del cliente
        5. Persistir cambios con cliente.save()
    
    JUSTIFICACIÓN:
        - Cumple regla de negocio: todo pedido debe descontar saldo
        - Previene saldos negativos con validación previa
        - Mantiene consistencia entre diferentes endpoints
        - Evita race conditions del double-save
    """
    # Calcular total del pedido
    productos = serializer.validated_data.get('productos', [])
    total = sum([p.precio for p in productos])
    cliente = self.request.user
    
    # ✅ Validar saldo suficiente ANTES de crear
    if cliente.saldo < total:
        raise ValidationError({'error': 'Saldo insuficiente'})
    
    # ✅ Guardar pedido UNA SOLA VEZ
    pedido = serializer.save(cliente=cliente, total=total)
    
    # ✅ Descontar saldo del cliente
    cliente.saldo -= total
    cliente.save()
```

##### 🎯 CUÁNDO USAR ESTE FORMATO:

- ✅ Corrección de bugs de lógica de negocio
- ✅ Modificación de validaciones críticas
- ✅ Cambios que afectan datos financieros (saldos, pagos, totales)
- ✅ Correcciones de race conditions o double-saves
- ✅ Fixes de inconsistencias entre diferentes partes del código

##### ❌ CUÁNDO NO ES NECESARIO:

- Cambios cosméticos o de formato
- Renombramiento de variables simple
- Agregado de logging
- Refactorización sin cambio de comportamiento

### Imports

#### Orden
1. Librerías estándar de Python
2. Django y terceros
3. Módulos locales

```python
from django.contrib.auth.models import AbstractUser  # Django
from django.db import models
from rest_framework import serializers              # Terceros
from .models import Usuario, Producto               # Local
```

---

## ✨ Buenas Prácticas

### 1. **Seguridad**

- ✅ Validar permisos en todas las vistas sensibles
- ✅ Sanitizar entrada de usuarios
- ✅ No exponer información sensible en respuestas de error
- ✅ Usar HTTPS en producción
- ✅ Implementar rate limiting para APIs públicas

### 2. **Base de Datos**

- ✅ Crear migraciones después de cambios en modelos:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
- ✅ Usar `select_related()` y `prefetch_related()` para optimizar queries
- ✅ Indexar campos de búsqueda frecuente
- ✅ Usar transacciones para operaciones críticas:
  ```python
  from django.db import transaction
  
  with transaction.atomic():
      # operaciones que deben ser atómicas
  ```

### 3. **API REST**

- ✅ Usar verbos HTTP correctamente:
  - GET: Lectura
  - POST: Creación
  - PUT/PATCH: Actualización
  - DELETE: Eliminación
- ✅ Retornar códigos de estado apropiados:
  - 200: OK
  - 201: Created
  - 400: Bad Request
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found
  - 500: Server Error
- ✅ Proveer mensajes de error descriptivos
- ✅ Documentar endpoints (considerar Swagger/OpenAPI)

### 4. **Testing**

- ✅ Escribir tests para:
  - Modelos (validaciones, métodos personalizados)
  - Vistas (endpoints, permisos)
  - Serializadores (validaciones)
- ✅ Usar fixtures para datos de prueba
- ✅ Ejecutar tests antes de commits:
  ```bash
  python manage.py test
  ```

### 5. **Versionamiento**

- ✅ Usar Git para control de versiones
- ✅ Commits descriptivos en español:
  ```
  feat: agregar validación de saldo en pedidos
  fix: corregir cálculo de total en pedidos
  refactor: optimizar query de productos activos
  ```
- ✅ No versionar:
  - `venv/`, `env/`
  - `__pycache__/`
  - `*.pyc`
  - `.env` (variables de entorno)
  - `db.sqlite3`

### 6. **Desempeño**

- ✅ Paginar resultados grandes
- ✅ Usar caché para datos frecuentes
- ✅ Optimizar queries N+1
- ✅ Comprimir respuestas grandes
- ✅ Usar índices en base de datos

### 7. **Mantenibilidad**

- ✅ Código DRY (Don't Repeat Yourself)
- ✅ Funciones pequeñas y enfocadas
- ✅ Separar lógica de negocio de presentación
- ✅ Documentar decisiones arquitectónicas
- ✅ Mantener dependencias actualizadas

---

## 🔄 Flujo de Trabajo de Desarrollo

### 1. Crear Nueva Funcionalidad

```bash
# 1. Crear/modificar modelo
# Editar core/models.py

# 2. Crear migración
python manage.py makemigrations

# 3. Aplicar migración
python manage.py migrate

# 4. Crear/actualizar serializer
# Editar core/serializers.py

# 5. Crear/actualizar vista
# Editar core/views.py

# 6. Configurar URL
# Editar core/urls.py

# 7. Probar en admin (opcional)
# Editar core/admin.py

# 8. Ejecutar servidor de desarrollo
python manage.py runserver
```

### 2. Proceso de Testing

```bash
# Crear tests en core/tests.py
python manage.py test core

# Tests específicos
python manage.py test core.tests.TestUsuario
```

### 3. Deployment

```bash
# 1. Actualizar settings para producción
# DEBUG = False
# ALLOWED_HOSTS = ['tu-dominio.com']

# 2. Colectar archivos estáticos
python manage.py collectstatic

# 3. Migrar base de datos de producción
python manage.py migrate --settings=burritos_project.settings_prod

# 4. Crear superusuario
python manage.py createsuperuser
```

---

## 📝 Endpoints Disponibles

### Usuarios
- `GET /api/usuarios/` - Listar usuarios
- `POST /api/usuarios/` - Crear usuario
- `GET /api/usuarios/{id}/` - Detalle usuario
- `PUT /api/usuarios/{id}/` - Actualizar usuario
- `DELETE /api/usuarios/{id}/` - Eliminar usuario

### Productos
- `GET /api/productos/` - Listar productos activos
- `POST /api/productos/` - Crear producto
- `GET /api/productos/{id}/` - Detalle producto
- `PUT /api/productos/{id}/` - Actualizar producto
- `DELETE /api/productos/{id}/` - Eliminar producto

### Categorías
- `GET /api/categorias/` - Listar categorías
- `POST /api/categorias/` - Crear categoría
- `GET /api/categorias/{id}/` - Detalle categoría
- `PUT /api/categorias/{id}/` - Actualizar categoría
- `DELETE /api/categorias/{id}/` - Eliminar categoría

### Pedidos
- `GET /api/pedidos/` - Listar pedidos
- `POST /api/pedidos/` - Crear pedido
- `GET /api/pedidos/{id}/` - Detalle pedido
- `PUT /api/pedidos/{id}/` - Actualizar pedido
- `DELETE /api/pedidos/{id}/` - Eliminar pedido
- `POST /api/crear_pedido/` - Crear pedido con validación de saldo

### 🆕 Endpoints para Clientes (Nuevos - 2025-10-26)

Según requerimientos, el cliente puede:
- ✅ Hacer pedidos
- ✅ Consultar sus pedidos actuales y pasados
- ✅ Consultar menú
- ✅ Recargar saldo a su cuenta
- ✅ Consultar su saldo

#### Menú
- `GET /api/cliente/menu/` - Consultar menú completo (categorías con productos activos)

#### Pedidos del Cliente
- `GET /api/cliente/mis-pedidos/` - Consultar todos mis pedidos
- `GET /api/cliente/mis-pedidos/?tipo=actuales` - Solo pedidos actuales (pendiente, en_proceso)
- `GET /api/cliente/mis-pedidos/?tipo=pasados` - Solo pedidos pasados (completado, cancelado)
- `GET /api/cliente/mis-pedidos/?estatus=pendiente` - Filtrar por estatus específico

#### Saldo
- `GET /api/cliente/mi-saldo/` - Consultar mi saldo actual
- `POST /api/cliente/recargar-saldo/` - Recargar saldo
  ```json
  {
    "monto": 100.00
  }
  ```

---

## 🚀 Mejoras Futuras Recomendadas

1. **Autenticación y Autorización**
   - Implementar JWT tokens
   - Sistema de permisos por rol
   - Endpoints de login/logout/registro

2. **Testing**
   - Suite completa de tests unitarios
   - Tests de integración
   - Coverage mínimo del 80%

3. **Documentación API**
   - Integrar Swagger/OpenAPI
   - Documentación interactiva

4. **Optimizaciones**
   - Sistema de caché (Redis)
   - Paginación en todos los listados
   - Compresión de respuestas

5. **Funcionalidades**
   - Sistema de notificaciones
   - Historial de pedidos
   - Calificaciones de productos
   - Cupones de descuento
   - Tracking de pedidos en tiempo real

6. **DevOps**
   - Dockerización
   - CI/CD pipeline
   - Monitoreo y logging
   - Backups automatizados

---

## 🆕 Funcionalidades para Clientes (Implementadas 2025-10-26)

### Requerimientos
El usuario cliente debe poder:
- ✅ Hacer pedidos
- ✅ Consultar sus pedidos actuales y pasados
- ✅ Consultar menú
- ✅ Recargar saldo a su cuenta
- ✅ Consultar su saldo

### Endpoints Implementados

#### 1. Consultar Menú
**Endpoint:** `GET /api/cliente/menu/`

**Descripción:** Muestra el menú completo organizado por categorías con productos activos.

**Respuesta:**
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
    }
  ],
  "total_categorias": 3
}
```

**Vista:** `MenuView` en `core/views.py`  
**Serializer:** `CategoriaConProductosSerializer`, `ProductoMenuSerializer`

---

#### 2. Consultar Mis Pedidos
**Endpoint:** `GET /api/cliente/mis-pedidos/`

**Autenticación:** Requerida (`IsAuthenticated`)

**Filtros disponibles:**
- `?tipo=actuales` - Solo pedidos pendiente o en_proceso
- `?tipo=pasados` - Solo pedidos completado o cancelado
- `?estatus=pendiente` - Filtrar por estatus específico

**Ejemplos:**
```bash
# Todos mis pedidos
GET /api/cliente/mis-pedidos/

# Solo pedidos actuales
GET /api/cliente/mis-pedidos/?tipo=actuales

# Solo pedidos pasados
GET /api/cliente/mis-pedidos/?tipo=pasados

# Solo pedidos pendientes
GET /api/cliente/mis-pedidos/?estatus=pendiente
```

**Respuesta:**
```json
{
  "pedidos": [
    {
      "id": 5,
      "cliente": 2,
      "cliente_nombre": "juan",
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

**Vista:** `MisPedidosView` en `core/views.py`  
**Serializer:** `PedidoDetalleSerializer`

---

#### 3. Consultar Mi Saldo
**Endpoint:** `GET /api/cliente/mi-saldo/`

**Autenticación:** Requerida (`IsAuthenticated`)

**Respuesta:**
```json
{
  "saldo": 500.00,
  "usuario": "juan",
  "email": "juan@example.com",
  "fecha_consulta": "2025-10-26T18:30:00Z"
}
```

**Vista:** `MiSaldoView` en `core/views.py`

---

#### 4. Recargar Saldo
**Endpoint:** `POST /api/cliente/recargar-saldo/`

**Autenticación:** Requerida (`IsAuthenticated`)

**Body:**
```json
{
  "monto": 100.00
}
```

**Validaciones:**
- ✅ Monto debe ser positivo (mínimo $0.01)
- ✅ Monto máximo: $10,000
- ✅ Debe ser número decimal válido

**Respuesta exitosa:**
```json
{
  "mensaje": "Saldo recargado exitosamente",
  "monto_recargado": 100.00,
  "saldo_anterior": 500.00,
  "saldo_actual": 600.00,
  "usuario": "juan",
  "fecha_recarga": "2025-10-26T18:30:00Z"
}
```

**Respuesta de error:**
```json
{
  "error": "Datos inválidos",
  "detalles": {
    "monto": ["El monto debe ser mayor a 0"]
  }
}
```

**Vista:** `RecargarSaldoView` en `core/views.py`  
**Serializer:** `RecargarSaldoSerializer`

---

### Serializadores Nuevos

#### ProductoMenuSerializer
Serializer simplificado para mostrar productos en el menú (solo información esencial).

#### CategoriaConProductosSerializer
Serializer que incluye productos activos de cada categoría (para mostrar menú organizado).

#### PedidoDetalleSerializer
Serializer detallado que incluye:
- Nombre del cliente
- Lista de productos con nombre y precio
- Toda la información del pedido

#### RecargarSaldoSerializer
Serializer de validación para recargas:
- Valida monto positivo (Decimal)
- Valida monto máximo $10,000
- Mensajes de error descriptivos

---

### Reglas de Negocio Aplicadas

#### ✅ Separación de Responsabilidades
- Endpoints específicos para clientes bajo `/api/cliente/`
- Vistas separadas para cada funcionalidad
- Serializadores específicos según el caso de uso

#### ✅ Seguridad
- `IsAuthenticated` en endpoints que requieren autenticación
- Filtrado automático por cliente (solo ve sus propios datos)
- Validación de montos en recargas

#### ✅ Buenas Prácticas según rules.md
- Comentarios descriptivos en español con emojis
- Validaciones antes de procesar datos
- Mensajes de error descriptivos
- Uso de `DecimalField` para dinero
- Uso de `timezone.now()` para fechas
- Filtros con `prefetch_related` para optimizar queries

#### ✅ Consistencia
- Formato de respuesta JSON consistente
- Códigos de estado HTTP apropiados
- Nomenclatura descriptiva para endpoints
- Serializers con campos explícitos

---

### Archivos Modificados

1. **core/serializers.py**
   - ➕ `ProductoMenuSerializer` - Menú simplificado
   - ➕ `CategoriaConProductosSerializer` - Categorías con productos
   - ➕ `PedidoDetalleSerializer` - Pedidos con detalles
   - ➕ `RecargarSaldoSerializer` - Validación de recarga
   - ✏️ `ProductoSerializer` - Agregado `categoria_nombre`

2. **core/views.py**
   - ➕ `MenuView` - Consultar menú
   - ➕ `MisPedidosView` - Consultar mis pedidos
   - ➕ `MiSaldoView` - Consultar mi saldo
   - ➕ `RecargarSaldoView` - Recargar saldo

3. **core/urls.py**
   - ➕ `cliente/menu/` - Ruta para menú
   - ➕ `cliente/mis-pedidos/` - Ruta para pedidos
   - ➕ `cliente/mi-saldo/` - Ruta para saldo
   - ➕ `cliente/recargar-saldo/` - Ruta para recarga

4. **rules.md**
   - ✏️ Sección de endpoints actualizada
   - ➕ Sección "Funcionalidades para Clientes"

---

### Ejemplos de Uso con curl

```bash
# 1. Consultar menú (sin autenticación requerida)
curl -X GET http://localhost:8000/api/cliente/menu/

# 2. Consultar mi saldo (requiere autenticación)
curl -X GET http://localhost:8000/api/cliente/mi-saldo/ \
  -H "Authorization: Token tu_token_aqui"

# 3. Recargar saldo
curl -X POST http://localhost:8000/api/cliente/recargar-saldo/ \
  -H "Authorization: Token tu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{"monto": 100.00}'

# 4. Consultar mis pedidos actuales
curl -X GET "http://localhost:8000/api/cliente/mis-pedidos/?tipo=actuales" \
  -H "Authorization: Token tu_token_aqui"

# 5. Consultar todos mis pedidos
curl -X GET http://localhost:8000/api/cliente/mis-pedidos/ \
  -H "Authorization: Token tu_token_aqui"
```

---

## 📞 Contacto y Soporte

Para dudas sobre este proyecto, consultar:
- Documentación oficial de Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Repositorio del proyecto: [Agregar URL]

---

**Última actualización:** 2025-10-26  
**Versión Django:** 5.2.7  
**Versión Python:** 3.x (recomendado 3.9+)

---

## 🐛 Historial de Correcciones de Bugs

### Bug #1: Saldo no se descontaba al crear pedido (2025-10-26)

**PROBLEMA DETECTADO:** Al crear un pedido desde el admin de Django, el total se guardaba en 0 y NO se descontaba del saldo del usuario.

**CAUSA RAÍZ:** 
- El método `save_model()` se ejecuta ANTES de guardar la relación ManyToMany con productos
- Al intentar calcular el total, `obj.productos.all()` estaba vacío = total de 0
- El saldo del cliente no se descontaba

**ARCHIVOS MODIFICADOS:**
- `core/admin.py` - Movida lógica de cálculo de total a `save_related()`
- `core/models.py` - Simplificado método `save()` del modelo Pedido
- `core/views.py` - YA tenía la corrección implementada en `PedidoViewSet.perform_create()`

**SOLUCIÓN IMPLEMENTADA:**

1. **En `core/models.py` (Pedido.save()):**
   - Simplificado: Solo guarda, no calcula total
   - El cálculo se hace en admin.py y views.py según corresponda

2. **En `core/admin.py`:**
   - Creado `PedidoForm` con validación en método `clean()`:
     - Valida que hay productos seleccionados
     - Calcula el total sumando precios de productos
     - Valida saldo suficiente del cliente
     - Muestra error detallado si saldo es insuficiente
   
   - Modificado `PedidoAdmin`:
     - `save_model()`: Solo guarda el pedido, marca si es nuevo
     - **`save_related()`**: DESPUÉS de guardar productos M2M:
       * Calcula total sumando precios (ahora SÍ existen productos)
       * Actualiza campo total del pedido
       * Descuenta total del saldo del cliente (solo al crear)
       * Muestra mensaje de éxito con total y saldo restante

3. **En `core/views.py` (ya estaba corregido):**
   - `PedidoViewSet.perform_create()`:
     - Calcula total ANTES de guardar
     - Valida saldo suficiente
     - Guarda pedido UNA SOLA VEZ
     - Descuenta total del saldo del cliente
     - Persiste cambios con `cliente.save()`
   
   - `CrearPedidoView.post()`:
     - Ya tenía implementada la lógica correcta de descuento

**REGLAS DE NEGOCIO APLICADAS:**
- ✅ Todo pedido debe descontar el total del saldo del cliente
- ✅ Se debe validar saldo suficiente ANTES de crear el pedido
- ✅ Consistencia entre admin y API
- ✅ Prevenir saldos negativos

**CÓDIGO ANTES (admin.py):**
```python
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'total', 'estatus', 'fecha')
    filter_horizontal = ('productos',)
    readonly_fields = ('total',)
    # ❌ NO validaba saldo
    # ❌ NO calculaba total correctamente (productos M2M aún no guardados)
    # ❌ NO descontaba saldo
```

**CÓDIGO DESPUÉS:**
```python
# models.py - Pedido.save() SIMPLIFICADO
def save(self, *args, **kwargs):
    # Solo guarda, no calcula total (lo hacen admin y views)
    super().save(*args, **kwargs)

# admin.py
class PedidoForm(forms.ModelForm):
    def clean(self):
        # ✅ Valida saldo suficiente ANTES de guardar
        productos = cleaned_data.get('productos')
        cliente = cleaned_data.get('cliente')
        total = sum([p.precio for p in productos])
        if cliente.saldo < total:
            raise ValidationError('Saldo insuficiente')

class PedidoAdmin(admin.ModelAdmin):
    form = PedidoForm
    
    def save_model(self, request, obj, form, change):
        # Solo guarda el pedido, marca si es nuevo
        super().save_model(request, obj, form, change)
        request._pedido_es_nuevo = not change
    
    def save_related(self, request, form, formsets, change):
        # ✅ DESPUÉS de guardar productos M2M
        super().save_related(request, form, formsets, change)
        
        obj = form.instance
        # ✅ Ahora SÍ existen productos, calcular total
        total = sum([p.precio for p in obj.productos.all()])
        obj.total = total
        obj.save(update_fields=['total'])
        
        # ✅ Descontar saldo solo al crear
        if request._pedido_es_nuevo:
            obj.cliente.saldo -= total
            obj.cliente.save()
```

**TESTING REALIZADO:**
- ✅ `python manage.py check`: Sin errores
- ✅ Crear pedido desde admin calcula total correctamente
- ✅ Crear pedido desde admin descuenta saldo correctamente
- ✅ Crear pedido desde API descuenta saldo correctamente
- ✅ Validación de saldo insuficiente funciona en ambos
- ✅ Mensajes de error son descriptivos y claros
- ✅ Al editar pedido NO se vuelve a descontar saldo

**PUNTOS CLAVE DE LA SOLUCIÓN:**
1. **save_model()** se ejecuta ANTES de guardar productos M2M → Solo guarda pedido
2. **save_related()** se ejecuta DESPUÉS de guardar productos M2M → Calcula total y descuenta saldo
3. Uso de `request._pedido_es_nuevo` para saber si es creación o edición
4. `update_fields=['total']` para guardar solo el campo total (eficiente)

**PRÓXIMOS PASOS RECOMENDADOS:**
- Implementar tests unitarios para validar descuento de saldo
- Considerar usar transacciones atómicas para operaciones críticas
- Agregar logs de auditoría para cambios de saldo

---

## 📄 Licencia

[Especificar licencia del proyecto]
