#!/bin/bash
# Script para actualizar archivos estáticos en PythonAnywhere

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Actualizando Archivos Estáticos - Burritos To Go         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Ir al directorio del proyecto
cd ~/burritos_to_go

# Activar virtualenv
echo "🔄 Activando virtualenv..."
source venv/bin/activate

# Actualizar código desde GitHub
echo "📦 Actualizando código desde GitHub..."
git pull origin main

# Limpiar y recolectar archivos estáticos
echo "🎨 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

# Verificar que se crearon los archivos
echo ""
echo "✅ Verificando archivos creados:"
echo "   Admin: $(ls -1 staticfiles/admin/ 2>/dev/null | wc -l) archivos"
echo "   REST Framework: $(ls -1 staticfiles/rest_framework/ 2>/dev/null | wc -l) archivos"

# Permisos
echo ""
echo "🔐 Configurando permisos..."
chmod -R 755 staticfiles/

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ COMPLETADO                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 SIGUIENTE PASO:"
echo "   1. Ve a la pestaña 'Web' en PythonAnywhere"
echo "   2. Click en el botón verde 'Reload'"
echo "   3. Verifica: https://pradodiazbackend.pythonanywhere.com/admin/"
echo ""
