from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from application.services.sqlServerConection import get_views
from langchain.memory import ConversationBufferMemory
import json
from application.config import config

personalidad = """
Eres un asistente llamado: Bot Triple A, que atenderá consultas de los usuarios relacionadas
con datos empresariales de una base de datos SQL Sever, tienes el siguiente flujo de trabajo:
1. Recibes una consulta en lenguaje natural.
2. Traducirás la consulta a una consulta SQL válida, usando las vistas y columnas disponibles en la base de datos.
3. Ejecutarás la consulta SQL en la base de datos.
4. Recibirás los resultados de la consulta SQL.
5. Convertirás los resultados de la consulta SQL en una respuesta en lenguaje natural, clara y concisa.
6. Responderás al usuario con la respuesta en lenguaje natural.

Usa emojis al responder, para hacer la conversación más amigable.
No debes responder nada que no esté relacionado con la base de datos.
"""

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
database_views = get_views()
memoria = ConversationBufferMemory()
memoria.chat_memory.add_ai_message(personalidad)


def limpiar_json_envoltura(texto: str) -> str:
    """
    Elimina las envolturas ```json al inicio y ``` al final de un bloque de texto.
    """
    texto = texto.strip()
    if texto.startswith("```json"):
        texto = texto[len("```json"):].lstrip()
    if texto.endswith("```"):
        texto = texto[:-3].rstrip()
    return texto

def human_query_to_sql(consulta: str):
    system_template = f"""
    Eres un traductor de lenguaje natural a T-SQL, 
    evita comentarios extras, solo traduce y devuelve 
    la respuesta en formato json.
    <schema>
    {database_views}
    </schema>
    """
    
    messages = [
        SystemMessage(f"{system_template}"),
        HumanMessage(f"{consulta}"),
    ]

    response = model.invoke(messages)
    response = limpiar_json_envoltura(response.content)
    response_dict = json.loads(response)
    return response_dict["query"]
    

def database_response_to_natural_language(response_from_database: list[dict], consulta: str):
    system_template = f"""
    Convierte la respuesta de la base de datos a lenguaje natural, amigable para el usuario.
    Responde de forma concisa y clara, evitando tecnicismos innecesarios.
    """
    
    messages = [
        SystemMessage(system_template),
        HumanMessage(f"Consulta: {consulta}"),
        HumanMessage(f"Respuesta de la base de datos: {response_from_database}")
    ]
    
    
    response = model.invoke(messages)
    return response.content