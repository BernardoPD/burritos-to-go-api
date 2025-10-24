from rest_framework import viewsets
from .models import Usuario, Producto, Categoria, Pedido
from .serializers import UsuarioSerializer
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Producto, Pedido
from .serializers import CrearPedidoSerializer

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