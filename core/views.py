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
    """
    ViewSet para gestión de usuarios (Admin).
    Estructura de respuesta estándar: {success, code, data, message}
    Requiere autenticación para todos los métodos
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'code': 200,
            'data': {
                'usuarios': serializer.data,
                'total': queryset.count()
            },
            'message': 'Usuarios obtenidos exitosamente'
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'code': 200,
            'data': serializer.data,
            'message': 'Usuario obtenido exitosamente'
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'code': 400,
                'data': serializer.errors,
                'message': 'Datos inválidos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        return Response({
            'success': True,
            'code': 201,
            'data': serializer.data,
            'message': 'Usuario creado exitosamente'
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'code': 400,
                'data': serializer.errors,
                'message': 'Datos inválidos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response({
            'success': True,
            'code': 200,
            'data': serializer.data,
            'message': 'Usuario actualizado exitosamente'
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'code': 200,
            'data': None,
            'message': 'Usuario eliminado exitosamente'
        }, status=status.HTTP_200_OK)

class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de productos.
    Estructura de respuesta estándar: {success, code, data, message}
    GET/LIST públicos, POST/PUT/DELETE requieren autenticación
    """
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoSerializer
    
    def get_permissions(self):
        """
        GET y LIST son públicos (para mostrar menú)
        POST, PUT, DELETE requieren autenticación
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'code': 200,
            'data': {
                'productos': serializer.data,
                'total': queryset.count()
            },
            'message': 'Productos obtenidos exitosamente'
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'code': 200,
            'data': serializer.data,
            'message': 'Producto obtenido exitosamente'
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'code': 400,
                'data': serializer.errors,
                'message': 'Datos inválidos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        return Response({
            'success': True,
            'code': 201,
            'data': serializer.data,
            'message': 'Producto creado exitosamente'
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'code': 400,
                'data': serializer.errors,
                'message': 'Datos inválidos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response({
            'success': True,
            'code': 200,
            'data': serializer.data,
            'message': 'Producto actualizado exitosamente'
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'code': 200,
            'data': None,
            'message': 'Producto eliminado exitosamente'
        }, status=status.HTTP_200_OK)

class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de categorías.
    Estructura de respuesta estándar: {success, code, data, message}
    GET/LIST públicos, POST/PUT/DELETE requieren autenticación
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    def get_permissions(self):
        """
        GET y LIST son públicos (para mostrar menú)
        POST, PUT, DELETE requieren autenticación
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'code': 200,
            'data': {
                'categorias': serializer.data,
                'total': queryset.count()
            },
            'message': 'Categorías obtenidas exitosamente'
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'code': 200,
            'data': serializer.data,
            'message': 'Categoría obtenida exitosamente'
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'code': 400,
                'data': serializer.errors,
                'message': 'Datos inválidos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        return Response({
            'success': True,
            'code': 201,
            'data': serializer.data,
            'message': 'Categoría creada exitosamente'
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'code': 400,
                'data': serializer.errors,
                'message': 'Datos inválidos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response({
            'success': True,
            'code': 200,
            'data': serializer.data,
            'message': 'Categoría actualizada exitosamente'
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'code': 200,
            'data': None,
            'message': 'Categoría eliminada exitosamente'
        }, status=status.HTTP_200_OK)

class PedidoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de pedidos.
    Estructura de respuesta estándar: {success, code, data, message}
    Requiere autenticación para todos los métodos
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'code': 200,
            'data': {
                'pedidos': serializer.data,
                'total': queryset.count()
            },
            'message': 'Pedidos obtenidos exitosamente'
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'code': 200,
            'data': serializer.data,
            'message': 'Pedido obtenido exitosamente'
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'code': 400,
                'data': serializer.errors,
                'message': 'Datos inválidos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar y descontar saldo
        productos = serializer.validated_data.get('productos', [])
        if not productos:
            return Response({
                'success': False,
                'code': 400,
                'data': None,
                'message': 'No se encontraron productos válidos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        total = sum([p.precio for p in productos])
        cliente = request.user
        
        if cliente.saldo < total:
            return Response({
                'success': False,
                'code': 400,
                'data': {
                    'saldo_actual': float(cliente.saldo),
                    'total_pedido': float(total),
                    'faltante': float(total - cliente.saldo)
                },
                'message': 'Saldo insuficiente'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear pedido
        pedido = serializer.save(cliente=cliente, total=total)
        cliente.saldo -= total
        cliente.save()
        
        return Response({
            'success': True,
            'code': 201,
            'data': {
                'pedido_id': pedido.id,
                'total': float(total),
                'productos': [{'id': p.id, 'nombre': p.nombre, 'precio': float(p.precio)} for p in productos],
                'saldo_restante': float(cliente.saldo)
            },
            'message': 'Pedido creado exitosamente'
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'code': 400,
                'data': serializer.errors,
                'message': 'Datos inválidos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response({
            'success': True,
            'code': 200,
            'data': serializer.data,
            'message': 'Pedido actualizado exitosamente'
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'code': 200,
            'data': None,
            'message': 'Pedido eliminado exitosamente'
        }, status=status.HTTP_200_OK)

class CrearPedidoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        productos_ids = request.data.get('productos', [])
        productos = Producto.objects.filter(id__in=productos_ids, activo=True)

        if not productos.exists():
            return Response({
                'success': False,
                'code': 400,
                'data': None,
                'message': 'No se encontraron productos válidos.'
            }, status=400)

        total = sum([p.precio for p in productos])
        cliente = request.user

        if cliente.saldo < total:
            return Response({
                'success': False,
                'code': 400,
                'data': {
                    'saldo_actual': float(cliente.saldo),
                    'total_pedido': float(total),
                    'faltante': float(total - cliente.saldo)
                },
                'message': 'Saldo insuficiente.'
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
            'success': True,
            'code': 200,
            'data': {
                'pedido_id': pedido.id,
                'total': float(total),
                'productos': [p.nombre for p in productos],
                'fecha': pedido.fecha,
                'saldo_restante': float(cliente.saldo)
            },
            'message': 'Pedido creado exitosamente.'
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
                'success': False,
                'code': 400,
                'data': serializer.errors,
                'message': 'Datos inválidos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data['user']
        
        # Crear o obtener token
        token, created = Token.objects.get_or_create(user=user)
        
        # Login en sesión
        login(request, user)
        
        return Response({
            'success': True,
            'code': 200,
            'data': {
                'token': token.key,
                'usuario': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'rol': user.rol,
                    'saldo': float(user.saldo)
                }
            },
            'message': 'Login exitoso'
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
                'success': False,
                'code': 400,
                'data': serializer.errors,
                'message': 'Datos inválidos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        
        # Crear token para el nuevo usuario
        token = Token.objects.create(user=user)
        
        # Login automático
        login(request, user)
        
        return Response({
            'success': True,
            'code': 201,
            'data': {
                'token': token.key,
                'usuario': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'rol': user.rol,
                    'saldo': float(user.saldo)
                }
            },
            'message': 'Usuario registrado exitosamente'
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
            'success': True,
            'code': 200,
            'data': None,
            'message': 'Sesión cerrada exitosamente'
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
        return Response({
            'success': True,
            'code': 200,
            'data': serializer.data,
            'message': 'Perfil obtenido exitosamente'
        })

# ==================== VISTAS PARA CLIENTES ====================

class MenuView(APIView):
    """
    Vista para consultar el menú completo.
    Muestra categorías con sus productos activos.
    
    GET /api/cliente/menu/
    
    Respuesta:
    {
        "success": true,
        "code": 200,
        "data": {
            "categorias": [...],
            "total_categorias": 5
        },
        "message": "Menú obtenido exitosamente"
    }
    """
    def get(self, request):
        # Obtener categorías con productos activos
        categorias = Categoria.objects.prefetch_related('producto_set').all()
        serializer = CategoriaConProductosSerializer(categorias, many=True)
        
        return Response({
            'success': True,
            'code': 200,
            'data': {
                'categorias': serializer.data,
                'total_categorias': categorias.count()
            },
            'message': 'Menú obtenido exitosamente'
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
            'success': True,
            'code': 200,
            'data': {
                'pedidos': serializer.data,
                'total': pedidos.count(),
                'filtros_aplicados': {
                    'tipo': tipo,
                    'estatus': estatus
                }
            },
            'message': 'Pedidos obtenidos exitosamente'
        })

class MiSaldoView(APIView):
    """
    Vista para consultar el saldo del cliente.
    
    GET /api/cliente/mi-saldo/
    
    Respuesta:
    {
        "success": true,
        "code": 200,
        "data": {
            "saldo": 500.00,
            "usuario": "juan",
            "email": "juan@example.com",
            "fecha_consulta": "2025-10-26T18:30:00"
        },
        "message": "Saldo obtenido exitosamente"
    }
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cliente = request.user
        
        return Response({
            'success': True,
            'code': 200,
            'data': {
                'saldo': float(cliente.saldo),
                'usuario': cliente.username,
                'email': cliente.email,
                'fecha_consulta': timezone.now()
            },
            'message': 'Saldo obtenido exitosamente'
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
                'success': False,
                'code': 400,
                'data': serializer.errors,
                'message': 'Datos inválidos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        monto = serializer.validated_data['monto']
        cliente = request.user
        saldo_anterior = cliente.saldo
        
        # Recargar saldo
        cliente.saldo += monto
        cliente.save()
        
        return Response({
            'success': True,
            'code': 200,
            'data': {
                'monto_recargado': float(monto),
                'saldo_anterior': float(saldo_anterior),
                'saldo_actual': float(cliente.saldo),
                'usuario': cliente.username,
                'fecha_recarga': timezone.now()
            },
            'message': 'Saldo recargado exitosamente'
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