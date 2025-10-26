from rest_framework import serializers
from .models import Usuario, Producto, Categoria, Pedido
from decimal import Decimal
from django.contrib.auth import authenticate

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'saldo']

# ==================== SERIALIZADORES DE AUTENTICACIÓN ====================

class LoginSerializer(serializers.Serializer):
    """
    Serializer para login de usuarios.
    Valida credenciales y retorna token de autenticación.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Credenciales inválidas')
            if not user.is_active:
                raise serializers.ValidationError('Usuario inactivo')
            data['user'] = user
        else:
            raise serializers.ValidationError('Debe incluir username y password')
        
        return data

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de nuevos usuarios (clientes).
    Solo permite crear usuarios con rol 'cliente'.
    """
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    password2 = serializers.CharField(write_only=True, required=True, label='Confirmar password')
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Las contraseñas no coinciden'})
        return data
    
    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este email ya está registrado')
        return value
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        # Crear usuario con rol de cliente por defecto
        user = Usuario.objects.create_user(
            **validated_data,
            rol='cliente',
            saldo=0.00
        )
        user.set_password(password)
        user.save()
        
        return user

class PerfilSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar el perfil completo del usuario.
    """
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 'saldo', 'date_joined']
        read_only_fields = ['id', 'username', 'rol', 'saldo', 'date_joined']

class ProductoSerializer(serializers.ModelSerializer):
    """Serializer para mostrar productos con información de categoría"""
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria', 'categoria_nombre', 'activo']

class ProductoMenuSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para mostrar el menú a clientes.
    Solo muestra productos activos con información esencial.
    """
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria_nombre']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class CategoriaConProductosSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar categorías con sus productos activos.
    Útil para mostrar el menú organizado por categorías.
    """
    productos = ProductoMenuSerializer(
        many=True, 
        read_only=True, 
        source='producto_set'  # Relación inversa
    )
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'productos']

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        extra_kwargs = {
            'cliente': {'read_only': True},
            'total': {'read_only': True}
        }

class PedidoDetalleSerializer(serializers.ModelSerializer):
    """
    Serializer detallado para mostrar pedidos con información completa.
    Incluye nombres de productos en lugar de solo IDs.
    """
    cliente_nombre = serializers.CharField(source='cliente.username', read_only=True)
    productos_detalle = serializers.SerializerMethodField()
    
    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'cliente_nombre', 'productos_detalle', 'total', 'estatus', 'fecha']
    
    def get_productos_detalle(self, obj):
        """Devuelve lista de productos con nombre y precio"""
        return [
            {
                'id': p.id,
                'nombre': p.nombre,
                'precio': float(p.precio)
            }
            for p in obj.productos.all()
        ]

class CrearPedidoSerializer(serializers.Serializer):
    productos = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )

    def validate_productos(self, value):
        productos = Producto.objects.filter(id__in=value, activo=True)
        if not productos.exists():
            raise serializers.ValidationError("No se encontraron productos válidos.")
        return value

class RecargarSaldoSerializer(serializers.Serializer):
    """
    Serializer para validar recarga de saldo.
    Solo acepta montos positivos.
    """
    monto = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        min_value=Decimal('0.01'),
        error_messages={
            'min_value': 'El monto debe ser mayor a 0',
            'invalid': 'Ingrese un monto válido'
        }
    )
    
    def validate_monto(self, value):
        """Validación adicional del monto"""
        if value > Decimal('10000'):
            raise serializers.ValidationError("El monto máximo de recarga es $10,000")
        return value