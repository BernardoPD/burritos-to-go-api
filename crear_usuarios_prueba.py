"""
Script para crear usuarios de prueba en Burritos To Go
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'burritos_project.settings')
django.setup()

from core.models import Usuario
from decimal import Decimal

def crear_usuarios():
    print("🌯 Creando usuarios de prueba...\n")
    
    # 1. Crear Admin
    if not Usuario.objects.filter(username='admin').exists():
        admin = Usuario.objects.create_superuser(
            username='admin',
            email='admin@burritos.com',
            password='admin123',
            first_name='Admin',
            last_name='Sistema'
        )
        admin.rol = 'admin'
        admin.saldo = Decimal('1000.00')
        admin.save()
        print("✅ Usuario Admin creado:")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"   Rol: {admin.rol}")
        print(f"   Saldo: ${admin.saldo}\n")
    else:
        print("ℹ️  Usuario 'admin' ya existe\n")
    
    # 2. Crear Cliente 1
    if not Usuario.objects.filter(username='cliente1').exists():
        cliente1 = Usuario.objects.create_user(
            username='cliente1',
            email='cliente1@example.com',
            password='password123',
            first_name='Juan',
            last_name='Pérez'
        )
        cliente1.rol = 'cliente'
        cliente1.saldo = Decimal('500.00')
        cliente1.save()
        print("✅ Usuario Cliente1 creado:")
        print(f"   Username: cliente1")
        print(f"   Password: password123")
        print(f"   Rol: {cliente1.rol}")
        print(f"   Saldo: ${cliente1.saldo}\n")
    else:
        print("ℹ️  Usuario 'cliente1' ya existe\n")
    
    # 3. Crear Cliente 2
    if not Usuario.objects.filter(username='cliente2').exists():
        cliente2 = Usuario.objects.create_user(
            username='cliente2',
            email='cliente2@example.com',
            password='password123',
            first_name='María',
            last_name='García'
        )
        cliente2.rol = 'cliente'
        cliente2.saldo = Decimal('300.00')
        cliente2.save()
        print("✅ Usuario Cliente2 creado:")
        print(f"   Username: cliente2")
        print(f"   Password: password123")
        print(f"   Rol: {cliente2.rol}")
        print(f"   Saldo: ${cliente2.saldo}\n")
    else:
        print("ℹ️  Usuario 'cliente2' ya existe\n")
    
    print("=" * 60)
    print("🎉 ¡Usuarios de prueba listos!")
    print("=" * 60)
    print("\n📋 RESUMEN DE CREDENCIALES:\n")
    print("🔐 ADMIN:")
    print("   Username: admin")
    print("   Password: admin123\n")
    print("👤 CLIENTE 1:")
    print("   Username: cliente1")
    print("   Password: password123\n")
    print("👤 CLIENTE 2:")
    print("   Username: cliente2")
    print("   Password: password123\n")
    print("=" * 60)

if __name__ == '__main__':
    crear_usuarios()
