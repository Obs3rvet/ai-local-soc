Markdown

# 🛡️ AI-Driven Local SOC (Security Operations Center)

> Un SOC local, privado y automatizado impulsado por Inteligencia Artificial (Ollama) para la detección de amenazas en entornos Linux.

---

## 📌 Descripción del Proyecto
Este proyecto implementa un Centro de Operaciones de Seguridad (SOC) ligero y completamente local. Utiliza **Python** para la monitorización de eventos del sistema operativo **Ubuntu**, procesando registros de autenticación en tiempo real e integrando modelos de lenguaje locales a través de **Ollama** (`llama3`) para clasificar comportamientos sospechosos, detectar ataques de fuerza bruta y generar alertas estructuradas en formato JSON sin comprometer la privacidad de los datos.

---

## 🏗️ Arquitectura del Sistema
El flujo operativo del SOC se divide en componentes modulares y privados:
1. **Colector / Monitor:** Un script en Python que lee y filtra eventos de autenticación (`auth.log` o logs simulados).
2. **Motor de Inferencia Local (Ollama):** Analiza por lotes los eventos recopilados aplicando lógica de análisis defensivo.
3. **Generación de Alertas:** Entrega reportes estructurados con niveles de severidad y recomendaciones de mitigación.

+------------------------+      Lectura de Logs       +------------------------+
|     Ubuntu Host        | -------------------------> |  ai-local-soc (Python) |
|  (/var/log/auth.log)   |                            +------------------------+
+------------------------+                                         |
Petición HTTP Local
(API REST)
v
+------------------------+
|   Ollama Local (LLM)   |
|      (Modelo llama3)   |
+------------------------+
|
Alerta Estructurada
(JSON Output)


---

## 📂 Estructura de Directorios
```text
ai-local-soc/
│
├── logs/                # Almacenamiento local de logs y simulaciones
├── src/
│   ├── test_ollama.py   # Script de verificación de conectividad con Ollama
│   ├── log_analyzer.py  # Analizador estático de registros y pruebas unitarias
│   └── live_soc.py      # Demonio de monitorización y alertas en tiempo real
│
├── .gitignore           # Archivos excluidos del control de versiones
├── requirements.txt     # Dependencias del proyecto Python
└── README.md            # Documentación oficial del proyecto

🚀 Guía de Instalación y Despliegue Rápido
1. Clonar el repositorio
Bash

git clone [https://github.com/tu-usuario/ai-local-soc.git](https://github.com/tu-usuario/ai-local-soc.git)
cd ai-local-soc

2. Configurar el entorno virtual e instalar dependencias
Bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Verificar que Ollama esté activo en local

Asegúrate de tener Ollama ejecutándose en tu host con el modelo llama3:
Bash

curl http://localhost:11434/api/tags

4. Ejecución del Monitor en Tiempo Real
Bash

python src/live_soc.py

⚔️ Escenarios de Validación y Pruebas

Puedes comprobar el funcionamiento del SOC inyectando eventos de prueba en el archivo de registro simulado:
Bash

echo "Jan 15 10:00:01 ubuntu-dev sshd[1234]: Failed password for invalid user admin from 10.0.2.15 port 55432 ssh2" >> logs/auth_simulation.log

El sistema detectará el umbral anómalo y generará una alerta estructurada en la terminal clasificada por la IA.
🔒 Buenas Prácticas de Seguridad Implementadas

    Privacidad Local: Ningún dato, traza de log ni métrica sale hacia servidores externos; todo el procesamiento de IA ocurre de manera local en el hardware del host.

    Control de Versiones Seguro: El archivo .gitignore previene la filtración accidental de registros sensibles o credenciales.
