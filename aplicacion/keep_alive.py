import datetime
import threading
from os import getenv
import time
import requests

def keep_alive():
    """Función para mantener la app activa haciendo ping periódico"""
    def ping():
        while True:
            try:
                url = getenv('APP_URL')
                response = requests.get(f"{url}/debug/health", timeout=10)
                print(f"[{datetime.datetime.now()}] Ping exitoso: {response.status_code}")
            except Exception as e:
                print(f"[{datetime.datetime.now()}] Error en ping: {e}")
            
            time.sleep(600)
    
    # Ejecutar en un hilo separado
    thread = threading.Thread(target=ping)
    thread.daemon = True
    thread.start()
    print("🔄 Servicio de keep-alive iniciado")