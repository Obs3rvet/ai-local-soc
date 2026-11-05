import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # Cambia esto si usas otro modelo (ej. 'mistral')

def test_connection():
    payload = {
        "model": MODEL_NAME,
        "prompt": "Responde únicamente con la palabra 'CONECTADO' si puedes leer este mensaje.",
        "stream": False
    }
    
    try:
        print(f"[*] Conectando a Ollama en {OLLAMA_URL} usando el modelo '{MODEL_NAME}'...")
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print("\n[+] ¡Conexión exitosa!")
        print("Respuesta del modelo:")
        print(result.get("response", "").strip())
        
    except requests.exceptions.ConnectionError:
        print("\n[-] Error: No se pudo conectar con Ollama. Asegúrate de que el servicio esté activo en local.")
    except Exception as e:
        print(f"\n[-] Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    test_connection()
