import re

# --- DETECTOR DE INCIDENTES SOC v2 - BASTIAN GALLARDO ---
# Este script analiza logs de servidor web para detectar ataques de fuerza bruta
# y extraer automaticamente la IP atacante (IoC) para su bloqueo en Firewall.

nombre_archivo = "servidor.log"

print("[+] Iniciando analisis de telemetria de red...")
print("-" * 60)

intentos_fallidos = 0

with open(nombre_archivo, "r") as archivo:
    for linea in archivo:
        # 1. Contamos cada intento fallido de acceso (HTTP 401)
        if "401" in linea:
            intentos_fallidos += 1
            print(f"[ALERTA] Intento de fuerza bruta detectado | Acumulado: {intentos_fallidos}")
        
        # 2. Si detecta un acceso exitoso (HTTP 200) tras fallos anteriores -> ALERTA CRITICA
        elif "200" in linea and intentos_fallidos > 0:
            # Usamos Expresiones Regulares (Regex) para aislar la direccion IP de la linea
            match = re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", linea)
            
            if match:
                ip_atacante = match.group(0)
                print("-" * 60)
                print(f"🚨 [ACCION SOC REQUERIDA] ¡COMPROMISO DE CUENTA DETECTADO!")
                print(f"👉 Bloquear IP en Firewall inmediatamente: {ip_atacante}")
                print(f"👉 Motivo: Acceso exitoso tras {intentos_fallidos} intentos fallidos (Brute Force Success).")
                print("-" * 60)

print("[+] Analisis finalizado con exito.")