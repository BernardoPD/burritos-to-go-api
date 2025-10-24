from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from django import forms
from .models import Pedido, Producto, Usuario, Categoria

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'total', 'estatus', 'fecha')
    list_filter = ('estatus', 'fecha')
    search_fields = ('cliente__username',)
    filter_horizontal = ('productos',)
    readonly_fields = ('total',)

# ✅ CORRECCIÓN 7: Eliminar save_related() innecesario
# JUSTIFICACIÓN: No aporta lógica adicional, solo llama al padre
# PREVIENE: Complejidad innecesaria en el código

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

