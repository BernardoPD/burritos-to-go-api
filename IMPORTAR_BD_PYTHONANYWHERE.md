# 📊 IMPORTAR BASE DE DATOS EN PYTHONANYWHERE

## ✅ Base de Datos Exportada

**Archivo:** `burritos_db_data.json`
**Tamaño:** 12.67 KB
**Formato:** JSON (Django dumpdata)
**Fecha:** 2025-11-06

---

## 🎯 MÉTODO 1: Importar Archivo JSON (RECOMENDADO)

Este es el método más sencillo y seguro.

### Paso 1: Subir el archivo a PythonAnywhere

**Opción A - Por interfaz web:**
1. Ve a la pestaña **"Files"** en PythonAnywhere
2. Navega a: `/home/pradodiazbackend/burritos_to_go/`
3. Click en **"Upload a file"**
4. Sube el archivo: `burritos_db_data.json`

**Opción B - Por comando (desde tu PC local):**
```bash
# Usando SCP (si tienes habilitado en PythonAnywhere)
scp burritos_db_data.json pradodiazbackend@ssh.pythonanywhere.com:/home/pradodiazbackend/burritos_to_go/
```

**Opción C - Por Git (MÁS FÁCIL):**
El archivo ya está en el proyecto, así que cuando clones el repo, ya lo tendrás.

---

### Paso 2: Importar los datos

En la **Bash Console** de PythonAnywhere:

```bash
cd ~/burritos_to_go
source venv/bin/activate

# IMPORTANTE: Primero hacer las migraciones
python manage.py migrate

# Ahora importar los datos
python manage.py loaddata burritos_db_data.json
```

**Salida esperada:**
```
Installed 45 object(s) from 1 fixture(s)
```

---

## 🎯 MÉTODO 2: Comenzar Base de Datos Vacía

Si prefieres empezar desde cero (sin datos de prueba):

```bash
cd ~/burritos_to_go
source venv/bin/activate

# Solo hacer migraciones
python manage.py migrate

# Crear superusuario nuevo
python manage.py createsuperuser
```

---

## 📋 DATOS QUE SE IMPORTAN

El archivo `burritos_db_data.json` contiene:

### ✅ Usuarios:
- **admin** (superusuario)
  - Email: tenor_prado@yahoo.com.mx
  - Saldo: $385.00
  
- **cliente** (usuario de prueba)
  - Nombre: Luis Ortega
  - Email: secretariaecoccurso@gmail.com
  - Saldo: $0.00

- **empleado1** (empleado de prueba)
  - Usuario: empleado1

- **cliente2** (cliente de prueba)
  - Usuario: cliente2
  - Saldo: $500.00

### ✅ Productos del Menú:
- Burrito Clásico de Carne - $50.00
- Burrito de Pollo - $45.00
- Burrito Vegetariano - $40.00
- Quesadilla - $35.00
- Tacos (3 piezas) - $30.00
- Nachos con Queso - $25.00
- Refresco - $15.00
- Agua - $10.00

### ✅ Pedidos de Prueba:
- Varios pedidos en diferentes estados (pendiente, en_preparacion, listo, entregado)

---

## ⚠️ IMPORTANTE: Contraseñas

Las contraseñas en el archivo exportado están encriptadas. **NO** puedes ver las contraseñas originales.

### Usuarios conocidos después de la importación:

**Para el admin:**
- Usuario: `admin`
- Password: Necesitarás cambiarla. Ejecuta:
```bash
python manage.py changepassword admin
```

**Para crear nuevos usuarios:**
```bash
python manage.py createsuperuser
```

---

## 🔄 COMANDOS COMPLETOS PASO A PASO

### Escenario 1: Importar con datos existentes

```bash
# 1. Ir al directorio del proyecto
cd ~/burritos_to_go

# 2. Activar virtualenv
source venv/bin/activate

# 3. Hacer migraciones
python manage.py makemigrations
python manage.py migrate

# 4. Importar datos
python manage.py loaddata burritos_db_data.json

# 5. (Opcional) Cambiar password del admin
python manage.py changepassword admin

# 6. Verificar que todo se importó
python manage.py shell
>>> from core.models import Usuario, Producto, Pedido
>>> print(f"Usuarios: {Usuario.objects.count()}")
>>> print(f"Productos: {Producto.objects.count()}")
>>> print(f"Pedidos: {Pedido.objects.count()}")
>>> exit()

# 7. Collectstatic
python manage.py collectstatic --noinput
```

### Escenario 2: Base de datos vacía (empezar desde cero)

```bash
# 1. Ir al directorio del proyecto
cd ~/burritos_to_go

# 2. Activar virtualenv
source venv/bin/activate

# 3. Hacer migraciones
python manage.py makemigrations
python manage.py migrate

# 4. Crear superusuario
python manage.py createsuperuser

# 5. Collectstatic
python manage.py collectstatic --noinput
```

---

## 🧪 VERIFICAR LA IMPORTACIÓN

### Método 1: Django shell

```bash
cd ~/burritos_to_go
source venv/bin/activate
python manage.py shell
```

```python
from core.models import Usuario, Producto, Pedido

# Contar registros
print(f"Usuarios: {Usuario.objects.count()}")
print(f"Productos: {Producto.objects.count()}")
print(f"Pedidos: {Pedido.objects.count()}")

# Ver productos
for p in Producto.objects.all():
    print(f"{p.nombre} - ${p.precio}")

# Ver usuarios
for u in Usuario.objects.all():
    print(f"{u.username} ({u.rol}) - Saldo: ${u.saldo}")

# Salir
exit()
```

### Método 2: Admin de Django

1. Ve a: `https://pradodiazbackend.pythonanywhere.com/admin/`
2. Inicia sesión con tu superusuario
3. Revisa las tablas de Usuarios, Productos y Pedidos

### Método 3: API

```bash
# Ver el menú
curl https://pradodiazbackend.pythonanywhere.com/api/clientes/menu/

# Ver usuarios (requiere admin)
curl https://pradodiazbackend.pythonanywhere.com/admin/
```

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "No such table"
```bash
# Hacer migraciones primero
python manage.py migrate
```

### Error: "IntegrityError"
```bash
# La base de datos ya tiene datos
# Opción 1: Borrar datos existentes
python manage.py flush

# Opción 2: Empezar con BD vacía (no importar)
```

### Error: "Could not load core.Usuario"
```bash
# Verificar que las migraciones estén hechas
python manage.py showmigrations
python manage.py migrate
```

### Quiero resetear todo
```bash
cd ~/burritos_to_go
source venv/bin/activate

# Borrar todos los datos
python manage.py flush

# Volver a importar
python manage.py loaddata burritos_db_data.json
```

---

## 📝 NOTAS ADICIONALES

### ¿Cuándo usar cada método?

**Usar importación (Método 1) si:**
- ✅ Quieres tener datos de prueba inmediatamente
- ✅ Quieres ver el menú ya poblado
- ✅ Necesitas probar rápidamente la API

**Empezar vacío (Método 2) si:**
- ✅ Quieres ingresar tus propios datos
- ✅ Es para producción real
- ✅ No quieres datos de prueba

---

## 🎯 RECOMENDACIÓN

Para el deployment inicial:

1. **Usa el Método 1** (importar datos)
2. Prueba que todo funcione
3. Si todo está bien, puedes:
   - Mantener los datos de prueba y agregar más
   - O hacer `flush` y empezar limpio

---

## 📄 ARCHIVO INCLUIDO

El archivo `burritos_db_data.json` ya está incluido en el repositorio de GitHub, así que cuando clones el proyecto en PythonAnywhere, automáticamente lo tendrás disponible.

**Ubicación en PythonAnywhere:**
```
/home/pradodiazbackend/burritos_to_go/burritos_db_data.json
```

---

## ✅ CHECKLIST DE IMPORTACIÓN

- [ ] Repositorio clonado en PythonAnywhere
- [ ] Virtual environment creado y activado
- [ ] Dependencias instaladas
- [ ] Base de datos MySQL creada
- [ ] settings.py configurado
- [ ] Migraciones ejecutadas: `python manage.py migrate`
- [ ] Datos importados: `python manage.py loaddata burritos_db_data.json`
- [ ] Verificado que hay datos: Django shell o admin
- [ ] Password del admin cambiado (si se necesita)
- [ ] Collectstatic ejecutado
- [ ] Web app configurada y reload
- [ ] Probado en el navegador ✅

---

**¡Los datos de tu base de datos local ya están listos para PythonAnywhere!** 🎉
