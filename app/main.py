from fastapi import FastAPI
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    host="db",
    database="notesdb",
    user="devops",
    password="devops"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    text VARCHAR(255)
)
""")

conn.commit()


@app.get("/")
def read_root():
    return {"message": "DevOps Notes API running with PostgreSQL"}


@app.get("/notes")
def get_notes():
    cursor.execute("SELECT * FROM notes")
    rows = cursor.fetchall()
    return rows


@app.post("/notes")
def add_note(note: str):
    cursor.execute("INSERT INTO notes (text) VALUES (%s)", (note,))
    conn.commit()
    return {"message": "note added"}