from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoViewSet,
    CategoriaViewSet,
    PedidoViewSet,
    UsuarioViewSet,
    CrearPedidoView,
    # Vistas para clientes (API)
    MenuView,
    MisPedidosView,
    MiSaldoView,
    RecargarSaldoView,
    # Vistas de autenticación
    LoginView,
    RegisterView,
    LogoutView,
    MiPerfilView,
    # Vistas web para panel de cliente
    cliente_dashboard,
    cliente_menu_view,
    cliente_hacer_pedido_view,
    cliente_mis_pedidos_view,
    cliente_recargar_saldo_view,
    cliente_logout_view,
    # Vista web para panel de admin
    admin_dashboard,
    # Vista para menú de APIs
    api_menu_view,
)

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    # ==================== MENÚ DE APIs ====================
    path('menu/', api_menu_view, name='api-menu'),
    
    # Rutas del router
    path('', include(router.urls)),
    
    # Ruta general de crear pedido
    path('crear_pedido/', CrearPedidoView.as_view(), name='crear_pedido'),
    
    # ==================== RUTAS DE AUTENTICACIÓN ====================
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/mi-perfil/', MiPerfilView.as_view(), name='auth-mi-perfil'),
    
    # ==================== RUTAS API PARA CLIENTES ====================
    # Consultar menú
    path('cliente/menu/', MenuView.as_view(), name='cliente-menu'),
    # Crear pedido (POST)
    path('cliente/crear-pedido/', CrearPedidoView.as_view(), name='cliente-crear-pedido'),
    # Consultar pedidos (actuales y pasados)
    path('cliente/mis-pedidos/', MisPedidosView.as_view(), name='cliente-mis-pedidos'),
    # Consultar saldo
    path('cliente/mi-saldo/', MiSaldoView.as_view(), name='cliente-mi-saldo'),
    # Recargar saldo
    path('cliente/recargar-saldo/', RecargarSaldoView.as_view(), name='cliente-recargar-saldo'),
    
    # ==================== RUTAS WEB PANEL DE CLIENTE ====================
    path('panel/', cliente_dashboard, name='cliente-dashboard'),
    path('panel/menu/', cliente_menu_view, name='cliente-menu-view'),
    path('panel/hacer-pedido/', cliente_hacer_pedido_view, name='cliente-hacer-pedido'),
    path('panel/mis-pedidos/', cliente_mis_pedidos_view, name='cliente-mis-pedidos-view'),
    path('panel/recargar-saldo/', cliente_recargar_saldo_view, name='cliente-recargar-saldo-view'),
    path('panel/logout/', cliente_logout_view, name='cliente-logout'),
    
    # ==================== RUTAS WEB PANEL DE ADMIN ====================
    path('admin-panel/', admin_dashboard, name='admin-dashboard'),
]