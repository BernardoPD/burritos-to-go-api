# 🌯 Burritos To Go - Migraciones de Base de Datos

## ✅ Estado: COMPLETADO

**Fecha:** 2025-10-24  
**Base de Datos:** MySQL (MariaDB 11.5.2)  
**Nombre BD:** burritos_db

---

## 📊 Resumen de Migraciones Aplicadas

### Migraciones Core (Aplicación Principal)
- ✅ **0001_initial** - Creación inicial de modelos
- ✅ **0002_alter_pedido_estatus_alter_pedido_fecha_and_more** - Ajustes en modelo Pedido
- ✅ **0003_alter_pedido_fecha** - Modificación campo fecha
- ✅ **0004_alter_pedido_total** - Modificación campo total

### Migraciones Django (Sistema)
- ✅ **admin** (3 migraciones) - Sistema de administración
- ✅ **auth** (12 migraciones) - Sistema de autenticación
- ✅ **contenttypes** (2 migraciones) - Tipos de contenido
- ✅ **sessions** (1 migración) - Manejo de sesiones

---

## 🗄️ Tablas Creadas en burritos_db

### 1. **core_usuario** - Tabla de Usuarios
Extiende AbstractUser de Django con campos personalizados.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | bigint (PK) | Identificador único |
| username | varchar(150) (UNIQUE) | Nombre de usuario |
| email | varchar(254) | Correo electrónico |
| password | varchar(128) | Contraseña encriptada |
| first_name | varchar(150) | Nombre |
| last_name | varchar(150) | Apellido |
| **rol** | varchar(10) | Rol: super/admin/cliente |
| **saldo** | decimal(10,2) | Saldo de la billetera |
| is_staff | tinyint(1) | Puede acceder al admin |
| is_superuser | tinyint(1) | Superusuario |
| is_active | tinyint(1) | Usuario activo |
| date_joined | datetime(6) | Fecha de registro |
| last_login | datetime(6) | Último inicio de sesión |

### 2. **core_categoria** - Categorías de Productos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | bigint (PK) | Identificador único |
| nombre | varchar(50) | Nombre de la categoría |

### 3. **core_producto** - Productos del Menú
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | bigint (PK) | Identificador único |
| nombre | varchar(100) | Nombre del producto |
| descripcion | longtext | Descripción detallada |
| precio | decimal(6,2) | Precio del producto |
| activo | tinyint(1) | Producto disponible (soft delete) |
| categoria_id | bigint (FK) | Referencia a core_categoria |

### 4. **core_pedido** - Pedidos de Clientes
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | bigint (PK) | Identificador único |
| cliente_id | bigint (FK) | Referencia a core_usuario |
| total | decimal(10,2) | Total del pedido |
| estatus | varchar(20) | Estado: pendiente/completado/cancelado |
| fecha | datetime(6) | Fecha y hora del pedido |

### 5. **core_pedido_productos** - Relación ManyToMany
Tabla intermedia para la relación muchos-a-muchos entre Pedidos y Productos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | bigint (PK) | Identificador único |
| pedido_id | bigint (FK) | Referencia a core_pedido |
| producto_id | bigint (FK) | Referencia a core_producto |

### Tablas Auxiliares de Django
- **core_usuario_groups** - Grupos de usuarios
- **core_usuario_user_permissions** - Permisos de usuarios
- **auth_group** - Grupos del sistema
- **auth_group_permissions** - Permisos de grupos
- **auth_permission** - Permisos del sistema
- **django_admin_log** - Log de acciones en admin
- **django_content_type** - Tipos de contenido
- **django_migrations** - Control de migraciones
- **django_session** - Sesiones de usuario

---

## 🔧 Configuración Aplicada

### Archivo: `burritos_project/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'burritos_db',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

AUTH_USER_MODEL = 'core.Usuario'
```

---

## 📝 Comandos Ejecutados

```bash
# 1. Instalar dependencia de MySQL
pip install mysqlclient

# 2. Crear base de datos (desde MySQL CLI)
CREATE DATABASE IF NOT EXISTS burritos_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 3. Generar archivos de migración (ya existían)
python manage.py makemigrations

# 4. Aplicar migraciones a la base de datos
python manage.py migrate

# 5. Verificar migraciones aplicadas
python manage.py showmigrations

# 6. Verificar estructura de tablas (script personalizado)
python verificar_tablas.py
```

---

## 🎯 Próximos Pasos Recomendados

1. **Crear Superusuario**
   ```bash
   python manage.py createsuperuser
   ```

2. **Poblar Base de Datos** (Opcional)
   - Crear categorías iniciales
   - Agregar productos de ejemplo
   - Crear usuarios de prueba

3. **Iniciar Servidor de Desarrollo**
   ```bash
   python manage.py runserver
   ```

4. **Acceder al Admin**
   - URL: http://127.0.0.1:8000/admin/
   - Usar credenciales del superusuario

5. **Probar Endpoints de la API**
   - Usuarios: http://127.0.0.1:8000/api/usuarios/
   - Productos: http://127.0.0.1:8000/api/productos/
   - Categorías: http://127.0.0.1:8000/api/categorias/
   - Pedidos: http://127.0.0.1:8000/api/pedidos/

---

## 🔍 Verificación de Integridad

### Relaciones de Base de Datos
- ✅ Usuario → Pedido (ForeignKey)
- ✅ Categoría → Producto (ForeignKey)
- ✅ Pedido ↔ Producto (ManyToMany)

### Índices Automáticos
- ✅ Primary Keys en todas las tablas
- ✅ Foreign Keys indexadas
- ✅ Unique constraint en username

### Campos con Valores por Defecto
- ✅ Usuario.rol = 'cliente'
- ✅ Usuario.saldo = 0.00
- ✅ Producto.activo = True
- ✅ Pedido.total = 0
- ✅ Pedido.estatus = 'pendiente'

---

## ⚠️ Notas Importantes

1. **Contraseña de Base de Datos**: La contraseña está configurada como '12345678'. En producción, usar variables de entorno.

2. **Modelo de Usuario Personalizado**: Se usa `AUTH_USER_MODEL = 'core.Usuario'` en lugar del User por defecto de Django.

3. **Soft Delete en Productos**: Los productos tienen campo `activo` para no eliminarlos físicamente.

4. **Charset UTF-8**: Base de datos configurada con utf8mb4 para soporte completo de caracteres Unicode.

5. **Strict Mode Warning**: Django advierte que MySQL Strict Mode no está activado. Considerar activarlo en producción.

---

## 📦 Dependencias Instaladas

- Django 5.2.7
- djangorestframework
- mysqlclient 2.2.7

---

## ✅ Checklist de Completado

- [x] Base de datos MySQL creada
- [x] mysqlclient instalado
- [x] Configuración de base de datos actualizada
- [x] Migraciones aplicadas correctamente
- [x] Todas las tablas creadas
- [x] Relaciones entre tablas establecidas
- [x] Estructura verificada
- [ ] Superusuario creado (pendiente)
- [ ] Datos de prueba cargados (pendiente)
- [ ] Servidor probado (pendiente)

---

**Estado Final:** ✅ BASE DE DATOS LISTA PARA USO
