"""
Script para exportar la base de datos de Burritos To Go
Compatible con MySQL local y para importar en PythonAnywhere
"""

import subprocess
import os
from datetime import datetime

def export_database():
    """Exporta la base de datos usando mysqldump"""
    
    # Configuración de tu base de datos local
    DB_USER = 'root'
    DB_PASSWORD = '12345678'
    DB_NAME = 'burritos_db'
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    
    # Nombre del archivo de backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'burritos_db_backup_{timestamp}.sql'
    
    # Comando mysqldump
    # Nota: Ajusta la ruta si mysqldump está en otro lugar
    mysqldump_paths = [
        'mysqldump',  # Si está en PATH
        r'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe',
        r'C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqldump.exe',
        r'C:\xampp\mysql\bin\mysqldump.exe',
    ]
    
    mysqldump_cmd = None
    for path in mysqldump_paths:
        if os.path.exists(path) or path == 'mysqldump':
            mysqldump_cmd = path
            break
    
    if not mysqldump_cmd:
        print("❌ Error: No se encontró mysqldump")
        print("\nOpciones:")
        print("1. Usa el método alternativo con Django (ver más abajo)")
        print("2. Instala MySQL y asegúrate de que mysqldump esté en PATH")
        return False
    
    try:
        # Comando de exportación
        cmd = [
            mysqldump_cmd,
            f'-u{DB_USER}',
            f'-p{DB_PASSWORD}',
            f'-h{DB_HOST}',
            f'-P{DB_PORT}',
            '--default-character-set=utf8mb4',
            '--single-transaction',
            '--quick',
            '--lock-tables=false',
            DB_NAME
        ]
        
        print(f"📦 Exportando base de datos '{DB_NAME}'...")
        
        with open(backup_file, 'w', encoding='utf8') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            file_size = os.path.getsize(backup_file)
            print(f"✅ Exportación exitosa!")
            print(f"📄 Archivo: {backup_file}")
            print(f"📊 Tamaño: {file_size / 1024:.2f} KB")
            print(f"\n🚀 Para importar en PythonAnywhere:")
            print(f"   1. Sube el archivo {backup_file}")
            print(f"   2. Ejecuta: mysql -u pradodiazbackend -p pradodiazbackend$burritos_db < {backup_file}")
            return True
        else:
            print(f"❌ Error al exportar: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def export_with_django():
    """Método alternativo usando Django"""
    print("\n🔄 Exportando con Django dumpdata...")
    
    try:
        cmd = [
            'python', 'manage.py', 'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '-e', 'contenttypes',
            '-e', 'auth.Permission',
            '--indent', '2'
        ]
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = f'burritos_db_data_{timestamp}.json'
        
        with open(json_file, 'w', encoding='utf8') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            file_size = os.path.getsize(json_file)
            print(f"✅ Exportación exitosa!")
            print(f"📄 Archivo: {json_file}")
            print(f"📊 Tamaño: {file_size / 1024:.2f} KB")
            print(f"\n🚀 Para importar en PythonAnywhere:")
            print(f"   1. Sube el archivo {json_file}")
            print(f"   2. Ejecuta: python manage.py loaddata {json_file}")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Exportador de Base de Datos - Burritos To Go             ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Intentar con mysqldump primero
    success = export_database()
    
    # Si falla, usar Django como alternativa
    if not success:
        print("\n" + "="*60)
        print("Intentando método alternativo con Django...")
        print("="*60)
        export_with_django()
