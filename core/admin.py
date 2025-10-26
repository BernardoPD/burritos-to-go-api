from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from django import forms
from .models import Pedido, Producto, Usuario, Categoria

class PedidoForm(forms.ModelForm):
    """
    Formulario personalizado para Pedido que valida saldo suficiente.
    """
    class Meta:
        model = Pedido
        fields = '__all__'
        exclude = ('total',)
    
    def clean(self):
        """
        PROBLEMA DETECTADO: Al crear pedido desde admin NO se descuenta saldo
        
        CÓDIGO ANTERIOR:
            No existía validación de saldo en el admin
        
        PROBLEMA:
            1. Se creaban pedidos sin validar saldo del cliente
            2. NO se descontaba el total del saldo del cliente
            3. Inconsistencia con API que SÍ valida y descuenta
        
        SOLUCIÓN IMPLEMENTADA:
            1. Validar que productos no esté vacío
            2. Calcular total sumando precios de productos
            3. Validar saldo suficiente del cliente
            4. Mostrar mensaje de error detallado si es insuficiente
        
        JUSTIFICACIÓN:
            - Cumple regla de negocio: todo pedido requiere saldo suficiente
            - Mantiene consistencia entre admin y API
            - Previene pedidos con saldo insuficiente
        """
        cleaned_data = super().clean()
        productos = cleaned_data.get('productos')
        cliente = cleaned_data.get('cliente')
        
        # ✅ Validar que hay productos seleccionados
        if not productos:
            raise ValidationError('Debe seleccionar al menos un producto.')
        
        # ✅ Calcular total del pedido
        total = sum([p.precio for p in productos])
        
        # ✅ Validar saldo suficiente del cliente
        if cliente and cliente.saldo < total:
            raise ValidationError({
                'cliente': f'Saldo insuficiente. Saldo actual: ${cliente.saldo}, Total pedido: ${total}, Faltante: ${total - cliente.saldo}'
            })
        
        return cleaned_data

class PedidoAdmin(admin.ModelAdmin):
    form = PedidoForm
    list_display = ('id', 'cliente', 'total', 'estatus', 'fecha')
    list_filter = ('estatus', 'fecha')
    search_fields = ('cliente__username',)
    filter_horizontal = ('productos',)
    readonly_fields = ('total',)
    
    def save_model(self, request, obj, form, change):
        """
        Guarda el pedido sin calcular el total aún.
        El total se calcula en save_related() después de guardar los productos.
        """
        # ✅ Guardar el pedido primero (sin calcular total todavía)
        super().save_model(request, obj, form, change)
        # Almacenar en request si es creación nueva para usar en save_related()
        request._pedido_es_nuevo = not change
    
    def save_related(self, request, form, formsets, change):
        """
        PROBLEMA DETECTADO: Total se quedaba en 0 al crear pedido
        
        CÓDIGO ANTERIOR:
            No se calculaba el total después de guardar productos
            No se descontaba saldo del cliente
        
        PROBLEMA:
            1. save_model() se ejecuta ANTES de guardar productos (M2M)
            2. El total se calculaba cuando productos aún estaba vacío = 0
            3. El saldo del cliente NO se descontaba
        
        SOLUCIÓN IMPLEMENTADA:
            1. Guardar relaciones M2M primero (productos)
            2. DESPUÉS calcular total sumando precios de productos
            3. Actualizar campo total del pedido
            4. Descontar total del saldo del cliente (solo al crear)
            5. Guardar cliente con saldo actualizado
            6. Mostrar mensaje con total y saldo restante
        
        JUSTIFICACIÓN:
            - save_related() se ejecuta DESPUÉS de guardar productos M2M
            - Aquí SÍ podemos acceder a obj.productos.all() correctamente
            - El total se calcula con los productos ya asociados
            - Cumple regla: todo pedido debe descontar saldo
            - Consistente con API (views.py)
        """
        # ✅ Primero guardar las relaciones M2M (productos)
        super().save_related(request, form, formsets, change)
        
        # ✅ Obtener el objeto pedido del formulario
        obj = form.instance
        
        # ✅ Calcular total sumando precios de productos (AHORA sí existen)
        productos = obj.productos.all()
        total = sum([p.precio for p in productos])
        
        # ✅ Actualizar el total del pedido
        obj.total = total
        obj.save(update_fields=['total'])
        
        # ✅ Descontar saldo del cliente (solo al crear, no al editar)
        if getattr(request, '_pedido_es_nuevo', False):
            cliente = obj.cliente
            cliente.saldo -= total
            cliente.save()
            
            # ✅ Mensaje de éxito con información detallada
            messages.success(request, 
                f'✅ Pedido creado exitosamente. Total: ${total}. Saldo restante del cliente: ${cliente.saldo}')
        else:
            # Al editar, también recalcular pero NO descontar (ya se descontó al crear)
            messages.success(request, f'✅ Pedido actualizado correctamente. Total: ${total}')

# Configuración de admin para Usuario
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'saldo', 'is_active', 'date_joined')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        ('Información de Usuario', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'password')
        }),
        ('Información de Negocio', {
            'fields': ('rol', 'saldo')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {
            'fields': ('date_joined', 'last_login')
        }),
    )

# Configuración de admin para Producto
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'activo')
    list_filter = ('activo', 'categoria')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('activo',)

# Configuración de admin para Categoria
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

# Registrar todos los modelos
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria, CategoriaAdmin)

