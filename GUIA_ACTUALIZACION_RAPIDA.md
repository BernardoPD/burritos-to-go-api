# 🚀 ACTUALIZACIÓN RÁPIDA PYTHONANYWHERE

## ✅ CAMBIOS SUBIDOS A GITHUB

```
Commit: 4e752d5
Mensaje: feat: APIs listas para Flutter - agregados categoria_id, rol_id, success y code
Archivos: 10 files changed, 2614 insertions
```

---

## 📋 PASOS PARA ACTUALIZAR EN PYTHONANYWHERE

### 1️⃣ Abrir Bash Console

Ve a: https://www.pythonanywhere.com/user/pradodiazbackend/consoles/

Click en **"Bash"**

---

### 2️⃣ Copiar y Pegar Estos Comandos

```bash
# Ir al proyecto
cd ~/burritos_to_go

# Activar virtualenv
source venv/bin/activate

# Actualizar código
git pull origin main

# Verificar cambios
python manage.py check

# Recolectar estáticos
python manage.py collectstatic --noinput

# Reload
touch /var/www/pradodiazbackend_pythonanywhere_com_wsgi.py
```

---

### 3️⃣ O Reload desde la Web

Ve a: https://www.pythonanywhere.com/user/pradodiazbackend/webapps/

Click en el botón verde: **"Reload pradodiazbackend.pythonanywhere.com"**

---

## 🧪 PROBAR LOS CAMBIOS

### Productos (con categoria_id):
```
https://pradodiazbackend.pythonanywhere.com/api/productos/
```

Debes ver:
```json
{
    "id": 1,
    "categoria_id": 1,  ← NUEVO
    "categoria_nombre": "Burritos"
}
```

### Usuarios (con rol_id):
```
https://pradodiazbackend.pythonanywhere.com/api/usuarios/
```

Debes ver:
```json
{
    "id": 1,
    "rol": "cliente",
    "rol_id": 2  ← NUEVO
}
```

---

## ✅ VERIFICACIÓN

Si todo está bien, deberías poder hacer login y ver:

```json
{
    "success": true,  ← NUEVO
    "code": 200,      ← NUEVO
    "mensaje": "Login exitoso",
    "token": "...",
    "usuario": {...}
}
```

---

## 📄 ARCHIVOS DE AYUDA

- **ACTUALIZAR_PYTHONANYWHERE.txt** - Comandos detallados
- **API_FLUTTER_FINAL.md** - Documentación completa de APIs
- **PRUEBAS_APIS.md** - Ejemplos de pruebas

---

¡Listo para Flutter! 🎉
