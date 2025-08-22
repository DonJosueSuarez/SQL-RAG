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
2. Traducirás la consulta a una consulta tipo T-SQL válida, usando las vistas y columnas disponibles en la base de datos.
3. Ejecutarás la consulta T-SQL en la base de datos.
4. Recibirás los resultados de la consulta T-SQL.
5. Convertirás los resultados de la consulta T-SQL en una respuesta en lenguaje natural, clara y concisa.
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

    # Solo agrega el system_template si la memoria está "vacía" (solo la personalidad)
    if len(memoria.chat_memory.messages) == 1:
        system_template = f"""
        Eres un traductor de lenguaje natural a T-SQL, 
        evita comentarios extras, solo traduce y devuelve 
        la respuesta en formato json.
        ejemplo:
            "sql": "Aquí va la consulta T-SQL generada"
        <schema>
        {database_views}
        </schema>
        Si el usuario no hace preguntas sobre la base de datos solo devuelve el json con el response.
        ejemplo:
            "response": "Aquí van tus comentarios de la consulta del usuario
        """
        memoria.chat_memory.add_ai_message(system_template)

    # Incluye historial de memoria
    messages = memoria.chat_memory.messages.copy()
    messages.append(HumanMessage(f"{consulta}"))

    response = model.invoke(messages)
    respuesta = response.content
    print(response.content)
    # Guarda el intercambio en memoria
    memoria.chat_memory.add_user_message(consulta)
    memoria.chat_memory.add_ai_message(response.content)
    try:
        response = limpiar_json_envoltura(response.content)
        response_dict = json.loads(response)
        if "sql" in response_dict:
            return response_dict["sql"]
        elif "response" in response_dict:
            return response_dict["response"]
    except:
        return respuesta
    

def database_response_to_natural_language(response_from_database: list[dict], consulta: str):
    system_template = f"""
    Convierte la respuesta de la base de datos a lenguaje natural, amigable para el usuario.
    Responde de forma concisa y clara, evitando tecnicismos innecesarios.
    """
    
    # Incluye historial de memoria
    messages = memoria.chat_memory.messages.copy()
    messages.append(SystemMessage(system_template))
    messages.append(HumanMessage(f"Consulta: {consulta}"))
    messages.append(HumanMessage(f"Respuesta de la base de datos: {response_from_database}"))

    response = model.invoke(messages)
    # Guarda el intercambio en memoria
    memoria.chat_memory.add_user_message(f"Consulta: {consulta}\nRespuesta de la base de datos: {response_from_database}")
    memoria.chat_memory.add_ai_message(response.content)
    return response.content