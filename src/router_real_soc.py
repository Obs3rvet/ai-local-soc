import socket
import requests
import json
import threading
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"
SYSLOG_PORT = 514
LOG_FILE = "logs/router_real.log"

# Palabras clave para filtrado rápido en memoria antes de invocar al LLM
ALERT_KEYWORDS = ["DROP", "REJECT", "DENY", "Failed", "invalid", "attack", "Unauthorized", "login failed"]

def analyze_with_ollama(logs_batch):
    prompt = f"""
    Eres un analista SOC defensivo. Analiza el siguiente lote de registros REALES de red/firewall provenientes del router principal:
    
    {logs_batch}
    
    Determina si hay algún intento de intrusión, escaneo de puertos, fuerza bruta o anomalía de seguridad.
    Responde estrictamente en formato JSON con la siguiente estructura:
    {{
      "attack_detected": true o false,
      "severity": "CRITICO", "ALTO", "MEDIO" o "BAJO",
      "source_ip": "IP origen sospechosa o 'N/A'",
      "summary": "Explicación corta del evento detectado",
      "recommended_action": "Acción recomendada para mitigar"
    }}
    """
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        return json.loads(response.json().get("response", "{}"))
    except Exception as e:
        print(f"[-] Error al comunicarse con Ollama: {e}")
        return None

def start_syslog_server():
    # Abrir socket UDP para escuchar los logs del router en el puerto 514
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(("0.0.0.0", SYSLOG_PORT))
        print(f"[+] Servidor Syslog REAL escuchando en UDP 0.0.0.0:{SYSLOG_PORT}...")
    except PermissionError:
        print(f"[-] Error: Para escuchar en el puerto {SYSLOG_PORT} necesitas ejecutar el script con sudo:")
        print(f"    sudo ../venv/bin/python src/router_real_soc.py")
        return

    buffer = []
    last_analysis = time.time()

    with open(LOG_FILE, "a") as log_file:
        while True:
            data, addr = sock.recvfrom(4096)
            message = data.decode('utf-8', errors='ignore').strip()
            log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] From {addr[0]}: {message}"
            
            # Guardar en archivo local
            log_file.write(log_entry + "\n")
            log_file.flush()
            print(f"[LOG RECIBIDO]: {log_entry}")

            # Filtrar si contiene patrones de alerta o sospecha
            if any(keyword.lower() in message.lower() for keyword in ALERT_KEYWORDS):
                buffer.append(log_entry)

            # Analizar con IA al acumular 3 eventos sospechosos o cada 15 segundos
            if len(buffer) >= 3 or (buffer and (time.time() - last_analysis > 15)):
                print("\n[!] Eventos sospechosos acumulados. Enviando a Ollama para análisis...")
                analysis = analyze_with_ollama("\n".join(buffer))
                
                if analysis:
                    print("\n" + "="*60)
                    print("🚨 ALERTA DE SEGURIDAD REAL DEL ROUTER 🚨")
                    print("="*60)
                    print(json.dumps(analysis, indent=4, ensure_ascii=False))
                    print("="*60 + "\n")
                
                buffer.clear()
                last_analysis = time.time()

if __name__ == "__main__":
    start_syslog_server()
