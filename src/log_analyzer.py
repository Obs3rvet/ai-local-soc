import requests
import json
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def analyze_log_entry(log_line):
    """
    Envía una línea o bloque de logs a Ollama para que actúe como analista SOC
    y determine si hay un comportamiento sospechoso o un ataque de fuerza bruta.
    """
    prompt = f"""
    Eres un analista SOC experto en ciberseguridad defensiva. 
    Analiza la siguiente línea de registro de autenticación de Linux (auth.log):
    
    "{log_line}"
    
    Responde estrictamente en formato JSON con la siguiente estructura:
    {{
      "is_suspicious": true o false,
      "threat_level": "BAJO", "MEDIO" o "ALTO",
      "attack_type": "Fuerza Bruta", "Login Exitoso", "Desconocido", etc.,
      "reason": "Breve explicación de por qué es o no sospechoso"
    }}
    """
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"  # Forzamos a Ollama a devolver un JSON válido
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return json.loads(result.get("response", "{}"))
    except Exception as e:
        print(f"[-] Error al comunicarse con Ollama: {e}")
        return None

if __name__ == "__main__":
    # Logs de prueba para simular tráfico normal y malicioso
    sample_logs = [
        "Accepted publickey for root from 192.168.1.50 port 52144 ssh2",
        "Failed password for invalid user admin from 192.168.1.100 port 44212 ssh2",
        "Failed password for invalid user admin from 192.168.1.100 port 44214 ssh2",
        "Failed password for invalid user admin from 192.168.1.100 port 44216 ssh2",
    ]

    print("[*] Iniciando simulación de análisis de SOC con IA...\n")
    
    for log in sample_logs:
        print(f"Analizando log: {log}")
        analysis = analyze_log_entry(log)
        
        if analysis:
            print("Resultado del Análisis:")
            print(json.dumps(analysis, indent=4, ensure_ascii=False))
            print("-" * 50)
        time.sleep(1)
