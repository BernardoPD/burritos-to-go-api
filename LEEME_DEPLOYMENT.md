# 🌯 DEPLOYMENT EN PYTHONANYWHERE - BURRITOS TO GO

## 📦 ¿Qué Necesitas?

Tu proyecto Django ya está **100% listo** para subirse a PythonAnywhere. Se han creado todos los archivos necesarios:

### ✅ Archivos Creados para Deployment:

1. **`PASO_A_PASO_PYTHONANYWHERE.md`** ⭐ **¡EMPIEZA AQUÍ!**
   - Guía rápida en 5 pasos
   - La más fácil de seguir
   
2. **`GUIA_DEPLOYMENT_FINAL.md`**
   - Guía completa y detallada
   - Incluye troubleshooting
   
3. **`CHECKLIST_DEPLOYMENT.md`**
   - Lista de verificación paso a paso
   - Para no olvidar nada
   
4. **`pythonanywhere_wsgi.py`**
   - Archivo WSGI listo para copiar
   
5. **`.env.example`**
   - Ejemplo de variables de entorno
   
6. **`requirements.txt`**
   - Actualizado con todas las dependencias

---

## 🚀 Inicio Rápido (3 Minutos)

### 1️⃣ Sube el Código a GitHub
```bash
git add .
git commit -m "Ready for PythonAnywhere"
git push origin main
```

### 2️⃣ Regístrate en PythonAnywhere
- Ve a: https://www.pythonanywhere.com/
- Crea cuenta gratuita
- Anota tu usuario

### 3️⃣ Sigue la Guía
- Abre: **`PASO_A_PASO_PYTHONANYWHERE.md`**
- Sigue los 5 pasos
- ¡Listo!

---

## 📁 Estructura de Archivos de Deployment

```
burritos_to_go/
├── 📄 PASO_A_PASO_PYTHONANYWHERE.md    ⭐ EMPIEZA AQUÍ
├── 📄 GUIA_DEPLOYMENT_FINAL.md         (Guía completa)
├── 📄 CHECKLIST_DEPLOYMENT.md          (Lista verificación)
├── 📄 pythonanywhere_wsgi.py           (Para copiar en WSGI)
├── 📄 .env.example                     (Variables de entorno)
├── 📄 requirements.txt                 (Dependencias)
├── 📁 burritos_project/
│   ├── settings.py                     (Configurar DB aquí)
│   └── wsgi.py
├── 📁 core/
│   ├── models.py
│   ├── views.py
│   └── ...
└── manage.py
```

---

## ⚙️ Lo Que Tienes Que Cambiar

### En PythonAnywhere, actualizar en `settings.py`:

```python
# 1. Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TU_USUARIO$burritos_db',      # ⚠️ CAMBIAR
        'USER': 'TU_USUARIO',                  # ⚠️ CAMBIAR
        'PASSWORD': 'tu_password_mysql',       # ⚠️ CAMBIAR
        'HOST': 'TU_USUARIO.mysql.pythonanywhere-services.com',  # ⚠️ CAMBIAR
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

# 2. Seguridad
DEBUG = False
ALLOWED_HOSTS = ['TU_USUARIO.pythonanywhere.com']  # ⚠️ CAMBIAR
```

---

## 🎯 URLs Finales

Cuando esté desplegado, tu API estará en:

```
https://TU_USUARIO.pythonanywhere.com
```

**Endpoints principales:**
- Admin: `/admin/`
- API: `/api/`
- Registro Cliente: `/api/clientes/registro/`
- Login Cliente: `/api/clientes/login/`
- Menú: `/api/clientes/menu/`
- Pedidos: `/api/clientes/pedidos/`

---

## 📱 Para Usar en tu App Móvil

```dart
// Flutter
class ApiService {
  static const String baseUrl = 'https://TU_USUARIO.pythonanywhere.com';
  static const String apiUrl = '$baseUrl/api/clientes/';
}
```

```javascript
// React Native
const BASE_URL = 'https://TU_USUARIO.pythonanywhere.com';
const API_URL = `${BASE_URL}/api/clientes/`;
```

---

## ✅ Checklist Rápido

Antes de empezar:
- [ ] Código funcionando localmente
- [ ] Git configurado
- [ ] Cuenta en PythonAnywhere creada

Durante deployment:
- [ ] Código subido/clonado en PythonAnywhere
- [ ] Virtual environment creado
- [ ] Dependencias instaladas
- [ ] Base de datos MySQL creada
- [ ] `settings.py` actualizado
- [ ] Migraciones ejecutadas
- [ ] Web app configurada
- [ ] WSGI configurado
- [ ] Static files configurados

Verificación:
- [ ] Sitio carga sin errores
- [ ] Admin funciona
- [ ] API responde
- [ ] Puedes hacer login

---

## 🆘 ¿Problemas?

### Error común: "No module named 'mysqlclient'"
```bash
source venv/bin/activate
pip install mysqlclient
# Reload en la web app
```

### Error común: "Database connection failed"
- Verifica que el nombre sea: `TU_USUARIO$burritos_db`
- Verifica el host: `TU_USUARIO.mysql.pythonanywhere-services.com`
- Verifica tu contraseña MySQL

### Ver logs:
- Pestaña "Web" → "Error log"
- Pestaña "Web" → "Server log"

---

## 📚 Documentación

### Para el Equipo de Frontend:
- `DOCUMENTACION_API_COMPLETA_FLUTTER.md` - Todos los endpoints
- `GUIA_ENDPOINTS_CLIENTE.md` - Endpoints para clientes
- `PAQUETE_PARA_FRONTEND.md` - Info completa para frontend

### Para Administradores:
- `PANELES_WEB_COMPLETOS.md` - Paneles web del sistema
- `MENU_VISUAL_RESUMEN.md` - Gestión del menú

---

## 🎓 Nivel de Dificultad

- **Principiante**: Sigue `PASO_A_PASO_PYTHONANYWHERE.md`
- **Intermedio**: Usa `GUIA_DEPLOYMENT_FINAL.md`
- **Experto**: Solo necesitas el `CHECKLIST_DEPLOYMENT.md`

---

## ⏱️ Tiempo Estimado

- **Primera vez**: 20-30 minutos
- **Con experiencia**: 10 minutos
- **Actualizaciones**: 3 minutos

---

## 💰 Costos

**¡GRATIS!** ✅
- Cuenta Beginner de PythonAnywhere es completamente gratuita
- Incluye:
  - 1 aplicación web
  - Base de datos MySQL
  - 512 MB de espacio
  - HTTPS incluido
  - Sin tarjeta de crédito necesaria

---

## 🚀 ¡Empieza Ahora!

1. Abre: **`PASO_A_PASO_PYTHONANYWHERE.md`**
2. Sigue los pasos
3. En 20 minutos tendrás tu API en línea

---

## 📞 Soporte

Documentación oficial de PythonAnywhere:
- https://help.pythonanywhere.com/
- https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/

---

**¡Tu API de Burritos To Go lista para producción!** 🎉

_Actualizado: $(date)_
