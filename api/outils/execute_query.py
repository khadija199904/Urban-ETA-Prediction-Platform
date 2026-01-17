from sqlalchemy import text
def execute_query(db,query):
    rows = db.execute(text(query)).fetchall()
    return rows
