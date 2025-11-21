#!/bin/bash
################################################################################
# Script de Actualización Automática para PythonAnywhere
# Usuario: pradodiazbackend
# Proyecto: burritos_to_go
################################################################################

echo "════════════════════════════════════════════════════════════════════════"
echo "  ACTUALIZACIÓN AUTOMÁTICA - APIS FLUTTER"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mensajes de éxito
success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Función para mensajes de error
error() {
    echo -e "${RED}✗${NC} $1"
}

# Función para mensajes de información
info() {
    echo -e "${YELLOW}→${NC} $1"
}

################################################################################
# PASO 1: Navegar al proyecto
################################################################################
echo ""
info "PASO 1: Navegando al proyecto..."
cd ~/burritos_to_go || { error "No se pudo acceder al directorio"; exit 1; }
success "Directorio: $(pwd)"

################################################################################
# PASO 2: Activar virtualenv
################################################################################
echo ""
info "PASO 2: Activando virtualenv..."
source venv/bin/activate || { error "No se pudo activar virtualenv"; exit 1; }
success "Virtualenv activado"

################################################################################
# PASO 3: Hacer backup
################################################################################
echo ""
info "PASO 3: Haciendo backup de archivos..."
cp core/serializers.py core/serializers.py.backup-$(date +%Y%m%d-%H%M%S)
cp core/views.py core/views.py.backup-$(date +%Y%m%d-%H%M%S)
cp core/urls.py core/urls.py.backup-$(date +%Y%m%d-%H%M%S)
success "Backup creado"

################################################################################
# PASO 4: Actualizar código desde GitHub
################################################################################
echo ""
info "PASO 4: Obteniendo cambios desde GitHub..."
git fetch origin || { error "Error en git fetch"; exit 1; }
success "Fetch completado"

echo ""
info "Aplicando cambios..."
git pull origin main || { error "Error en git pull"; exit 1; }
success "Código actualizado"

################################################################################
# PASO 5: Verificar cambios
################################################################################
echo ""
info "PASO 5: Verificando último commit..."
git log --oneline -1
success "Último commit verificado"

################################################################################
# PASO 6: Reinstalar dependencias
################################################################################
echo ""
info "PASO 6: Verificando dependencias..."
pip install -r requirements.txt -q
success "Dependencias actualizadas"

################################################################################
# PASO 7: Aplicar migraciones
################################################################################
echo ""
info "PASO 7: Aplicando migraciones..."
python manage.py migrate
success "Migraciones aplicadas"

################################################################################
# PASO 8: Recolectar archivos estáticos
################################################################################
echo ""
info "PASO 8: Recolectando archivos estáticos..."
python manage.py collectstatic --noinput
success "Archivos estáticos actualizados"

################################################################################
# PASO 9: Verificar que no hay errores
################################################################################
echo ""
info "PASO 9: Verificando integridad del proyecto..."
python manage.py check || { error "Hay errores en el proyecto"; exit 1; }
success "Sin errores detectados"

################################################################################
# PASO 10: Reload de la aplicación
################################################################################
echo ""
info "PASO 10: Recargando aplicación web..."
touch /var/www/pradodiazbackend_pythonanywhere_com_wsgi.py
success "Aplicación recargada"

################################################################################
# PASO 11: Verificar cambios implementados
################################################################################
echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo "  VERIFICACIÓN DE CAMBIOS"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

info "Verificando ProductoSerializer..."
if python -c "from core.serializers import ProductoSerializer; s=ProductoSerializer(); assert 'categoria_id' in s.get_fields()" 2>/dev/null; then
    success "ProductoSerializer - categoria_id: OK"
else
    error "ProductoSerializer - categoria_id: NO ENCONTRADO"
fi

info "Verificando UsuarioSerializer..."
if python -c "from core.serializers import UsuarioSerializer; s=UsuarioSerializer(); assert 'rol_id' in s.get_fields()" 2>/dev/null; then
    success "UsuarioSerializer - rol_id: OK"
else
    error "UsuarioSerializer - rol_id: NO ENCONTRADO"
fi

################################################################################
# RESUMEN FINAL
################################################################################
echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo "  ✅ ACTUALIZACIÓN COMPLETADA"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "Cambios implementados:"
echo "  ✓ ProductoSerializer - categoria_id agregado"
echo "  ✓ UsuarioSerializer - rol_id agregado"
echo "  ✓ LoginView - success y code agregados"
echo "  ✓ RegisterView - success y code agregados"
echo ""
echo "URLs para probar:"
echo "  → https://pradodiazbackend.pythonanywhere.com/api/productos/"
echo "  → https://pradodiazbackend.pythonanywhere.com/api/usuarios/"
echo "  → https://pradodiazbackend.pythonanywhere.com/api/menu/"
echo ""
echo "Documentación:"
echo "  → API_FLUTTER_FINAL.md - Documentación completa"
echo "  → PRUEBAS_APIS.md - Ejemplos de pruebas"
echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo "  ¡LISTO PARA FLUTTER! 🚀"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
