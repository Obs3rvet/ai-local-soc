import time
import requests
import json
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"
LOG_FILE = "logs/auth_simulation.log" # Usaremos una simulación local para no requerir sudo continuo

def analyze_batch(log_batch):
    prompt = f"""
    Eres un analista SOC defensivo. Revisa el siguiente bloque de registros de autenticación recabados en tiempo real:
    
    {log_batch}
    
    Determina si se está llevando a cabo un ataque (como Fuerza Bruta por SSH).
    Responde estrictamente en formato JSON con la siguiente estructura:
    {{
      "attack_detected": true o false,
      "severity": "CRITICO", "ALTO", "MEDIO" o "BAJO",
      "attacker_ip": "IP detectada o 'Desconocida'",
      "summary": "Resumen ejecutivo del incidente y acción recomendada"
    }}
    """
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return json.loads(response.json().get("response", "{}"))
    except Exception as e:
        print(f"[-] Error llamando a Ollama: {e}")
        return None

def monitor_log():
    # Asegurarse de que el archivo existe
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
        
    print(f"[*] Escuchando eventos en tiempo real en: {LOG_FILE}...")
    
    with open(LOG_FILE, 'r') as f:
        # Ir al final del archivo
        f.seek(0, os.SEEK_END)
        
        buffer = []
        last_analysis = time.time()
        
        while True:
            line = f.readline()
            if line:
                if "Failed password" in line or "invalid user" in line:
                    buffer.append(line.strip())
                    print(f"[!] Capturado evento de autenticación fallida...")
            else:
                time.sleep(0.5)
            
            # Si acumulamos 3 o más logs fallidos o pasaron 10 segundos con registros pendientes
            if len(buffer) >= 3 or (buffer and (time.time() - last_analysis > 10)):
                print("\n[+] Umbral de alerta alcanzado. Enviando ráfaga a Ollama para análisis de incidente...")
                logs_text = "\n".join(buffer)
                
                result = analyze_batch(logs_text)
                if result:
                    print("\n" + "="*60)
                    print("🚨 ALERTA DE SEGURIDAD SOC DECTECTADA 🚨")
                    print("="*60)
                    print(json.dumps(result, indent=4, ensure_ascii=False))
                    print("="*60 + "\n")
                
                buffer.clear()
                last_analysis = time.time()

if __name__ == "__main__":
    monitor_log()
