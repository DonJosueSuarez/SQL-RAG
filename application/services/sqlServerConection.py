from sqlalchemy import create_engine, text
from sqlalchemy import inspect
from application.config import config

engine = create_engine(config.SQL_SERVER_URL)

def get_views():
    inspector = inspect(engine)
    view_names = inspector.get_view_names()
    #print("Views in the database:", view_names)
    return {view: get_columns_and_types(view) for view in view_names}

def get_columns_and_types(view_name: str):
    inspector = inspect(engine)
    columns = inspector.get_columns(view_name)
    result = [f"{column['name']} ({column['type']})" for column in columns]
    #print(result)
    return result

def execute_query(query: str):
    with engine.connect() as connection:
        result = connection.execute(text(query))
        response = [dict(zip(result.keys(), row)) for row in result]
        return response