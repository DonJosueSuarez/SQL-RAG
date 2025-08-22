from fastapi import APIRouter
from application.services.llmConection import human_query_to_sql, database_response_to_natural_language
from application.services.sqlServerConection import execute_query
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    
router = APIRouter()

@router.post("/execute-query")
async def execute_query_endpoint(request: QueryRequest) -> dict[str, str]:
    print("Received request:", request)
    consulta = request.query
    sql = human_query_to_sql(consulta)
    try:
        respuesta_db = execute_query(sql)
        respuesta_gemini = database_response_to_natural_language(respuesta_db, consulta)
        return {"response": respuesta_gemini}
    except:
        return {"response": sql}
