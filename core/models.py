from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from decimal import Decimal

class Usuario(AbstractUser):
    ROLES = (
        ('super', 'Súper Usuario'),
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='cliente')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} (${self.precio})"

class Pedido(models.Model):
    cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    productos = models.ManyToManyField('Producto')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estatus = models.CharField(max_length=20, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:  # Solo al crear
            super().save(*args, **kwargs)  # Necesario para poder usar .productos
            self.total = sum(p.precio for p in self.productos.all())
            super().save(update_fields=['total'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username}"

