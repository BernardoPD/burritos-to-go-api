# 📋 INSTRUCCIONES PARA ACTUALIZAR PYTHONANYWHERE

## 🚀 OPCIÓN 1: SCRIPT AUTOMÁTICO (RECOMENDADO)

### Paso 1: Abrir Bash Console
Ve a: https://www.pythonanywhere.com/user/pradodiazbackend/consoles/

Click en **"Bash"**

### Paso 2: Subir el script
En la Bash console de PythonAnywhere:

```bash
cd ~/burritos_to_go
```

Luego copia y pega TODO este contenido:

```bash
cat > actualizar.sh << 'ENDOFSCRIPT'
#!/bin/bash
echo "════════════════════════════════════════════════════════════════════════"
echo "  ACTUALIZACIÓN AUTOMÁTICA - APIS FLUTTER"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
cd ~/burritos_to_go
source venv/bin/activate
echo "✓ Activando virtualenv..."
echo ""
echo "→ Haciendo backup..."
cp core/serializers.py core/serializers.py.backup-$(date +%Y%m%d)
cp core/views.py core/views.py.backup-$(date +%Y%m%d)
echo "✓ Backup creado"
echo ""
echo "→ Actualizando código..."
git fetch origin
git pull origin main
echo "✓ Código actualizado"
echo ""
echo "→ Verificando proyecto..."
python manage.py check
echo ""
echo "→ Recolectando estáticos..."
python manage.py collectstatic --noinput
echo "✓ Estáticos actualizados"
echo ""
echo "→ Recargando aplicación..."
touch /var/www/pradodiazbackend_pythonanywhere_com_wsgi.py
echo "✓ Aplicación recargada"
echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo "  ✅ ACTUALIZACIÓN COMPLETADA"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "Probar en:"
echo "  → https://pradodiazbackend.pythonanywhere.com/api/productos/"
echo "  → https://pradodiazbackend.pythonanywhere.com/api/usuarios/"
echo ""
ENDOFSCRIPT
```

### Paso 3: Ejecutar el script

```bash
chmod +x actualizar.sh
./actualizar.sh
```

---

## 🔧 OPCIÓN 2: COMANDOS MANUALES (COPIA Y PEGA)

Si prefieres ejecutar los comandos uno por uno:

```bash
# 1. Ir al proyecto
cd ~/burritos_to_go

# 2. Activar virtualenv
source venv/bin/activate

# 3. Actualizar código
git pull origin main

# 4. Verificar
python manage.py check

# 5. Recolectar estáticos
python manage.py collectstatic --noinput

# 6. Reload
touch /var/www/pradodiazbackend_pythonanywhere_com_wsgi.py
```

---

## 🌐 OPCIÓN 3: RELOAD DESDE LA WEB

Si ya hiciste los comandos anteriores, solo necesitas recargar:

1. Ve a: https://www.pythonanywhere.com/user/pradodiazbackend/webapps/
2. Click en el botón verde: **"Reload pradodiazbackend.pythonanywhere.com"**

---

## ✅ VERIFICACIÓN

Después de actualizar, abre estas URLs:

### 1. Productos (debe tener categoria_id):
```
https://pradodiazbackend.pythonanywhere.com/api/productos/
```

Debes ver:
```json
{
    "id": 1,
    "categoria": 1,
    "categoria_id": 1,  ← NUEVO
    "categoria_nombre": "Burritos"
}
```

### 2. Usuarios (debe tener rol_id):
```
https://pradodiazbackend.pythonanywhere.com/api/usuarios/
```

Debes ver:
```json
{
    "id": 1,
    "rol": "cliente",
    "rol_id": 2  ← NUEVO (1=admin, 2=cliente, 3=staff)
}
```

### 3. Login (debe tener success y code):

Usa Postman o curl:
```bash
curl -X POST https://pradodiazbackend.pythonanywhere.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"cliente1","password":"password123"}'
```

Debes ver:
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

## 🆘 SI HAY PROBLEMAS

Ver logs de error:
```bash
tail -n 50 /var/log/pradodiazbackend.pythonanywhere.com.error.log
```

Reiniciar desde cero:
```bash
cd ~/burritos_to_go
git reset --hard origin/main
source venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
touch /var/www/pradodiazbackend_pythonanywhere_com_wsgi.py
```

---

## 📞 RESUMEN

✅ Cambios subidos a GitHub: **4e752d5**
✅ Archivos listos para descargar en PythonAnywhere
✅ Script de actualización creado
✅ Documentación completa disponible

**Elige la opción que prefieras y ejecútala en PythonAnywhere** 🚀
