# Chatbot para consulta a base de Datos
Este proyecto usa el gestor de paquetes **uv**

## Instalación **uv**
```PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Sincronización del proyecto ♻️
En tu terminal navega hasta la carpeta donde clonaste el repositorio, ingresa a la carpeta y ejecuta el comando:
```PowerShell
uv sync
```

## Crea el archivo *.env* 🔒
```env
SQL_SERVER_URL =
LANGSMITH_TRACING="true"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_PROJECT="nombre de tu proyecto"

LANGSMITH_API_KEY=
GOOGLE_API_KEY=
```

## Corre la API
Usa el comando: `uv run main.py`

## Visualiza el Front
Abre tu navegador y escribe
```url
http://127.0.0.1:8000
```

### Felicidades estás corriendo el proyecto 😊