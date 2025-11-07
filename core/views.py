from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import Usuario, Producto, Categoria, Pedido
from .serializers import UsuarioSerializer
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils import timezone
from .models import Producto, Pedido
from .serializers import CrearPedidoSerializer
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def perform_create(self, serializer):
        """
        PROBLEMA DETECTADO: No se descontaba el saldo del cliente al crear pedido
        
        CÓDIGO ANTERIOR:
            serializer.save(cliente=self.request.user)
            productos = serializer.validated_data.get('productos', [])
            total = sum([p.precio for p in productos])
            serializer.save(cliente=self.request.user, total=total)
        
        PROBLEMA: 
            1. Se guardaba dos veces el pedido (doble llamada a serializer.save())
            2. NO se validaba saldo suficiente del cliente
            3. NO se descontaba el total del saldo del cliente
            4. Inconsistencia con CrearPedidoView que SÍ descuenta saldo
        
        SOLUCIÓN IMPLEMENTADA:
            1. Calcular total ANTES de guardar
            2. Validar saldo suficiente del cliente
            3. Guardar pedido UNA SOLA VEZ con todos los datos
            4. Descontar total del saldo del cliente
            5. Persistir cambios en el cliente con save()
        
        JUSTIFICACIÓN:
            - Cumple regla de negocio: todo pedido debe descontar saldo
            - Previene saldos negativos con validación previa
            - Mantiene consistencia con CrearPedidoView
            - Evita double-save que podría causar race conditions
        """
        # Obtener productos y calcular total del pedido
        productos = serializer.validated_data.get('productos', [])
        total = sum([p.precio for p in productos])
        cliente = self.request.user
        
        # ✅ Validar saldo suficiente ANTES de crear el pedido
        if cliente.saldo < total:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({
                'error': 'Saldo insuficiente.',
                'saldo_actual': float(cliente.saldo),
                'total_pedido': float(total),
                'faltante': float(total - cliente.saldo)
            })
        
        # ✅ Guardar pedido con todos los datos (una sola vez)
        pedido = serializer.save(cliente=cliente, total=total)
        
        # ✅ Descontar total del saldo del cliente
        cliente.saldo -= total
        cliente.save()
        
        # ✅ El saldo del cliente ahora refleja correctamente el pago del pedido

class CrearPedidoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        productos_ids = request.data.get('productos', [])
        productos = Producto.objects.filter(id__in=productos_ids, activo=True)

        if not productos.exists():
            return Response({'error': 'No se encontraron productos válidos.'}, status=400)

        total = sum([p.precio for p in productos])
        cliente = request.user

        if cliente.saldo < total:
            return Response({
                'error': 'Saldo insuficiente.',
                'saldo_actual': cliente.saldo,
                'total_pedido': total,
                'faltante': round(total - cliente.saldo, 2)
            }, status=400)

        pedido = Pedido.objects.create(
            cliente=cliente,
            total=total,
            estatus='pendiente',
            fecha=timezone.now()
        )
        pedido.productos.set(productos)
        cliente.saldo -= total
        cliente.save()

        return Response({
            'mensaje': 'Pedido creado exitosamente.',
            'pedido_id': pedido.id,
            'total': total,
            'productos': [p.nombre for p in productos],
            'fecha': pedido.fecha,
            'saldo_restante': cliente.saldo
        })

# ==================== VISTAS DE AUTENTICACIÓN ====================

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    Vista para login de usuarios.
    
    POST /api/auth/login/
    {
        "username": "cliente1",
        "password": "password123"
    }
    
    Retorna token de autenticación y datos del usuario.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'error': 'Datos inválidos',
                'detalles': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data['user']
        
        # Crear o obtener token
        token, created = Token.objects.get_or_create(user=user)
        
        # Login en sesión
        login(request, user)
        
        return Response({
            'mensaje': 'Login exitoso',
            'token': token.key,
            'usuario': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'rol': user.rol,
                'saldo': float(user.saldo)
            }
        }, status=status.HTTP_200_OK)

class RegisterView(APIView):
    """
    Vista para registro de nuevos usuarios (clientes).
    
    POST /api/auth/register/
    {
        "username": "cliente1",
        "email": "cliente1@example.com",
        "password": "password123",
        "password2": "password123",
        "first_name": "Juan",
        "last_name": "Pérez"
    }
    
    Crea usuario con rol 'cliente' y saldo inicial de $0.00
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'error': 'Datos inválidos',
                'detalles': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        
        # Crear token para el nuevo usuario
        token = Token.objects.create(user=user)
        
        # Login automático
        login(request, user)
        
        return Response({
            'mensaje': 'Usuario registrado exitosamente',
            'token': token.key,
            'usuario': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'rol': user.rol,
                'saldo': float(user.saldo)
            }
        }, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    """
    Vista para cerrar sesión.
    
    POST /api/auth/logout/
    
    Elimina el token de autenticación del usuario.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Eliminar token
        try:
            request.user.auth_token.delete()
        except:
            pass
        
        # Logout de sesión
        logout(request)
        
        return Response({
            'mensaje': 'Sesión cerrada exitosamente'
        }, status=status.HTTP_200_OK)

class MiPerfilView(APIView):
    """
    Vista para consultar el perfil del usuario autenticado.
    
    GET /api/auth/mi-perfil/
    
    Retorna información completa del usuario logueado.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = PerfilSerializer(request.user)
        return Response(serializer.data)

# ==================== VISTAS PARA CLIENTES ====================

class MenuView(APIView):
    """
    Vista para consultar el menú completo.
    Muestra categorías con sus productos activos.
    
    GET /api/cliente/menu/
    
    Respuesta:
    {
        "categorias": [
            {
                "id": 1,
                "nombre": "Burritos",
                "productos": [
                    {
                        "id": 1,
                        "nombre": "Burrito de Carne",
                        "descripcion": "...",
                        "precio": "80.00",
                        "categoria_nombre": "Burritos"
                    }
                ]
            }
        ]
    }
    """
    def get(self, request):
        # Obtener categorías con productos activos
        categorias = Categoria.objects.prefetch_related('producto_set').all()
        serializer = CategoriaConProductosSerializer(categorias, many=True)
        
        return Response({
            'categorias': serializer.data,
            'total_categorias': categorias.count()
        })

class MisPedidosView(APIView):
    """
    Vista para que el cliente consulte sus pedidos.
    
    GET /api/cliente/mis-pedidos/
    GET /api/cliente/mis-pedidos/?estatus=pendiente
    GET /api/cliente/mis-pedidos/?tipo=actuales  (pendiente o en_proceso)
    GET /api/cliente/mis-pedidos/?tipo=pasados   (completado o cancelado)
    
    Según rules.md:
    - El cliente puede consultar sus pedidos actuales y pasados
    - Se filtran solo los pedidos del cliente autenticado
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cliente = request.user
        
        # Filtrar por tipo (actuales o pasados)
        tipo = request.query_params.get('tipo', None)
        estatus = request.query_params.get('estatus', None)
        
        # Base queryset: solo pedidos del cliente
        pedidos = Pedido.objects.filter(cliente=cliente).order_by('-fecha')
        
        # Filtrar por tipo
        if tipo == 'actuales':
            # Pedidos actuales: pendiente o en_proceso
            pedidos = pedidos.filter(estatus__in=['pendiente', 'en_proceso'])
        elif tipo == 'pasados':
            # Pedidos pasados: completado o cancelado
            pedidos = pedidos.filter(estatus__in=['completado', 'cancelado'])
        
        # Filtrar por estatus específico
        if estatus:
            pedidos = pedidos.filter(estatus=estatus)
        
        serializer = PedidoDetalleSerializer(pedidos, many=True)
        
        return Response({
            'pedidos': serializer.data,
            'total': pedidos.count(),
            'filtros_aplicados': {
                'tipo': tipo,
                'estatus': estatus
            }
        })

class MiSaldoView(APIView):
    """
    Vista para consultar el saldo del cliente.
    
    GET /api/cliente/mi-saldo/
    
    Respuesta:
    {
        "saldo": "500.00",
        "usuario": "juan",
        "fecha_consulta": "2025-10-26T18:30:00"
    }
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cliente = request.user
        
        return Response({
            'saldo': float(cliente.saldo),
            'usuario': cliente.username,
            'email': cliente.email,
            'fecha_consulta': timezone.now()
        })

class RecargarSaldoView(APIView):
    """
    Vista para recargar saldo a la cuenta del cliente.
    
    POST /api/cliente/recargar-saldo/
    {
        "monto": 100.00
    }
    
    Validaciones según rules.md:
    - El monto debe ser positivo
    - El monto máximo es $10,000
    - Se actualiza el saldo del cliente
    - Se retorna el nuevo saldo
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = RecargarSaldoSerializer(data=request.data)
        
        # Validar datos
        if not serializer.is_valid():
            return Response({
                'error': 'Datos inválidos',
                'detalles': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        monto = serializer.validated_data['monto']
        cliente = request.user
        saldo_anterior = cliente.saldo
        
        # Recargar saldo
        cliente.saldo += monto
        cliente.save()
        
        return Response({
            'mensaje': 'Saldo recargado exitosamente',
            'monto_recargado': float(monto),
            'saldo_anterior': float(saldo_anterior),
            'saldo_actual': float(cliente.saldo),
            'usuario': cliente.username,
            'fecha_recarga': timezone.now()
        }, status=status.HTTP_200_OK)

# ==================== VISTAS WEB PARA PANEL DE CLIENTE ====================

@login_required
def cliente_dashboard(request):
    """Dashboard principal del cliente con interfaz web"""
    total_pedidos = Pedido.objects.filter(cliente=request.user).count()
    total_productos = Producto.objects.filter(activo=True).count()
    pedidos_recientes = Pedido.objects.filter(cliente=request.user).order_by('-fecha')[:5]
    
    return render(request, 'core/cliente_dashboard.html', {
        'total_pedidos': total_pedidos,
        'total_productos': total_productos,
        'pedidos_recientes': pedidos_recientes,
    })

@login_required
def cliente_menu_view(request):
    """Vista del menú con interfaz web"""
    categorias = Categoria.objects.prefetch_related('producto_set').all()
    return render(request, 'core/cliente_menu.html', {
        'categorias': categorias,
    })

@login_required
def cliente_hacer_pedido_view(request):
    """Vista para hacer pedido con interfaz web"""
    if request.method == 'POST':
        productos_ids = request.POST.getlist('productos')
        
        if not productos_ids:
            messages.error(request, 'Debes seleccionar al menos un producto')
            return redirect('cliente-hacer-pedido')
        
        productos = Producto.objects.filter(id__in=productos_ids, activo=True)
        
        if not productos.exists():
            messages.error(request, 'Los productos seleccionados no son válidos')
            return redirect('cliente-hacer-pedido')
        
        total = sum([p.precio for p in productos])
        cliente = request.user
        
        if cliente.saldo < total:
            messages.error(request, f'Saldo insuficiente. Necesitas ${total} pero solo tienes ${cliente.saldo}. Faltante: ${total - cliente.saldo}')
            return redirect('cliente-hacer-pedido')
        
        # Crear pedido
        pedido = Pedido.objects.create(
            cliente=cliente,
            total=total,
            estatus='pendiente',
            fecha=timezone.now()
        )
        pedido.productos.set(productos)
        
        # Descontar saldo
        cliente.saldo -= total
        cliente.save()
        
        messages.success(request, f'¡Pedido #{pedido.id} creado exitosamente! Total: ${total}. Saldo restante: ${cliente.saldo}')
        return redirect('cliente-mis-pedidos-view')
    
    # GET
    categorias = Categoria.objects.prefetch_related('producto_set').all()
    return render(request, 'core/cliente_hacer_pedido.html', {
        'categorias': categorias,
    })

@login_required
def cliente_mis_pedidos_view(request):
    """Vista de mis pedidos con interfaz web"""
    tipo = request.GET.get('tipo', None)
    
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha')
    
    if tipo == 'actuales':
        pedidos = pedidos.filter(estatus__in=['pendiente', 'en_proceso'])
    elif tipo == 'pasados':
        pedidos = pedidos.filter(estatus__in=['completado', 'cancelado'])
    
    return render(request, 'core/cliente_pedidos.html', {
        'pedidos': pedidos,
    })

@login_required
def cliente_recargar_saldo_view(request):
    """Vista para recargar saldo con interfaz web"""
    if request.method == 'POST':
        try:
            monto = Decimal(request.POST.get('monto', 0))
            
            if monto <= 0:
                messages.error(request, 'El monto debe ser mayor a 0')
                return redirect('cliente-recargar-saldo-view')
            
            if monto > Decimal('10000'):
                messages.error(request, 'El monto máximo de recarga es $10,000')
                return redirect('cliente-recargar-saldo-view')
            
            cliente = request.user
            saldo_anterior = cliente.saldo
            cliente.saldo += monto
            cliente.save()
            
            messages.success(request, f'¡Saldo recargado exitosamente! Agregaste ${monto}. Tu nuevo saldo es ${cliente.saldo}')
            return redirect('cliente-dashboard')
            
        except Exception as e:
            messages.error(request, 'Error al procesar la recarga. Verifica el monto ingresado.')
            return redirect('cliente-recargar-saldo-view')
    
    return render(request, 'core/cliente_recargar_saldo.html')

@login_required
def cliente_logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('/admin/login/')

# ==================== VISTAS WEB PARA PANEL DE ADMIN ====================

@login_required
def admin_dashboard(request):
    """Dashboard para administradores con estadísticas del sistema"""
    
    # Verificar si el usuario es admin o staff
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('cliente-dashboard')
    
    # Estadísticas generales
    total_usuarios = Usuario.objects.filter(rol='cliente').count()
    total_productos = Producto.objects.filter(activo=True).count()
    total_pedidos = Pedido.objects.count()
    ingresos_totales = Pedido.objects.filter(estatus='completado').aggregate(
        total=models.Sum('total')
    )['total'] or 0
    
    # Pedidos pendientes
    pedidos_pendientes = Pedido.objects.filter(
        estatus='pendiente'
    ).order_by('-fecha')[:10]
    
    # Últimos usuarios registrados
    ultimos_usuarios = Usuario.objects.order_by('-date_joined')[:5]
    
    # Estadísticas por categoría
    from django.db.models import Count
    categorias_stats = Categoria.objects.annotate(
        total=Count('producto')
    ).order_by('-total')
    
    return render(request, 'core/admin_dashboard.html', {
        'total_usuarios': total_usuarios,
        'total_productos': total_productos,
        'total_pedidos': total_pedidos,
        'ingresos_totales': ingresos_totales,
        'pedidos_pendientes': pedidos_pendientes,
        'ultimos_usuarios': ultimos_usuarios,
        'categorias_stats': categorias_stats,
    })

# ==================== VISTA PARA MENÚ DE APIs ====================
def api_menu_view(request):
    """
    Vista que muestra el menú interactivo de todas las APIs disponibles.
    Dividido en secciones: Admin, Cliente y Autenticación.
    """
    return render(request, 'api_menu.html')

def index_view(request):
    """
    Vista de inicio que muestra las opciones principales del sistema.
    """
    return render(request, 'index.html')

def login_page_view(request):
    """
    Vista que muestra la página de login personalizada.
    """
    return render(request, 'login.html')

def register_page_view(request):
    """
    Vista que muestra la página de registro personalizada.
    """
    return render(request, 'register.html')