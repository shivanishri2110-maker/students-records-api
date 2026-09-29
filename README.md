# Student Records API

A small REST API built with **Python, FastAPI, and SQLite**. It supports create, read, update, and delete operations for student records.

## What the terms mean

- **Backend:** the server-side program that receives requests, applies rules, and reads/writes data.
- **REST API:** a set of URLs and HTTP methods that programs use to communicate. For example, `POST /students` creates a record.
- **CRUD:** Create, Read, Update, Delete—the four basic operations for managing data.
- **Database:** organized storage. This project uses SQLite, which stores data in a local `students.db` file.
- **Validation:** checking submitted data (for example, year must be from 1 to 6) before saving it.
- **HTML/CSS/JavaScript:** tools for making a web page. They are not required for this backend mini project; FastAPI's interactive API page lets you try requests without building a separate website.

## Run it on Windows

1. Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/) and enable **Add Python to PATH** during installation.
2. Open PowerShell in this folder.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies and start the server:

   ```powershell
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

5. Visit **http://127.0.0.1:8000/docs**. The interactive page lets you try each endpoint. Stop the server with `Ctrl+C`.

## Endpoints

| Method | URL | Purpose |
|---|---|---|
| POST | `/students` | Add a student |
| GET | `/students` | List all students |
| GET | `/students/{id}` | Get one student |
| PUT | `/students/{id}` | Replace a student's details |
| DELETE | `/students/{id}` | Delete a student |

A student has `name`, `roll_number`, `department`, and `year`. Roll numbers must be unique; year must be between 1 and 6. Invalid input is rejected, duplicate roll numbers return HTTP 409, and missing IDs return HTTP 404.

## Example request

In `/docs`, open `POST /students`, choose **Try it out**, and submit:

```json
{
  "name": "Shivani Shri R D",
  "roll_number": "2127250601091",
  "department": "EEE",
  "year": 2
}
```

The API returns the saved student, including an automatically assigned `id`. The database file is created automatically the first time the app starts.

## Share it for the application

To submit a GitHub link, create a new public GitHub repository, upload the files in this folder, and paste that repository URL into the form. Do not upload `.venv` or `students.db`. This project is organized so you can upload it directly. A Google Drive folder link works too if their form accepts Drive links.
