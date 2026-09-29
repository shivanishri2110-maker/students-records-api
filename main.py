from contextlib import asynccontextmanager
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

DB_PATH = Path(__file__).with_name("students.db")


def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    with connect_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_number TEXT NOT NULL UNIQUE,
                department TEXT NOT NULL,
                year INTEGER NOT NULL CHECK (year BETWEEN 1 AND 6)
            )
        """)
    yield


app = FastAPI(
    title="Student Records API",
    description="A beginner-friendly REST API for managing student records.",
    version="1.0.0",
    lifespan=lifespan,
)


class StudentInput(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    roll_number: str = Field(min_length=1, max_length=30)
    department: str = Field(min_length=2, max_length=100)
    year: int = Field(ge=1, le=6, description="Study year (1 through 6)")


class Student(StudentInput):
    id: int


def row_to_student(row):
    return dict(row)


@app.get("/", tags=["Info"])
def home():
    return {"message": "Student Records API is running", "docs": "/docs"}


@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(student: StudentInput):
    try:
        with connect_db() as db:
            cursor = db.execute(
                "INSERT INTO students (name, roll_number, department, year) VALUES (?, ?, ?, ?)",
                (student.name.strip(), student.roll_number.strip(), student.department.strip(), student.year),
            )
            row = db.execute("SELECT * FROM students WHERE id = ?", (cursor.lastrowid,)).fetchone()
            return row_to_student(row)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="A student with that roll number already exists.")


@app.get("/students", response_model=list[Student], tags=["Students"])
def list_students():
    with connect_db() as db:
        rows = db.execute("SELECT * FROM students ORDER BY id").fetchall()
        return [row_to_student(row) for row in rows]


@app.get("/students/{student_id}", response_model=Student, tags=["Students"])
def get_student(student_id: int):
    with connect_db() as db:
        row = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    return row_to_student(row)


@app.put("/students/{student_id}", response_model=Student, tags=["Students"])
def update_student(student_id: int, student: StudentInput):
    try:
        with connect_db() as db:
            cursor = db.execute(
                "UPDATE students SET name = ?, roll_number = ?, department = ?, year = ? WHERE id = ?",
                (student.name.strip(), student.roll_number.strip(), student.department.strip(), student.year, student_id),
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Student not found.")
            row = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
            return row_to_student(row)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="A student with that roll number already exists.")


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
def delete_student(student_id: int):
    with connect_db() as db:
        cursor = db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
