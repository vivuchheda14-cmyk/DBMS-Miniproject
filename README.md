# DBMS Mini Project

A Python desktop application for managing an online education database using Tkinter and SQLite.

## Project Overview

This project simulates a simple online education management system with entities such as:

- Instructor
- Teaching / Non-Teaching Staff
- Student
- Assessment
- Grades
- Submission
- Fees
- Receipt

The application provides a GUI to insert, update, delete, retrieve, and view records from the database tables.

## Tech Stack

- Python
- Tkinter (GUI)
- SQLite3

## Features

- Dashboard summary for key tables
- Manage each database table through a dedicated window
- Insert new records
- Update existing records
- Delete records
- Retrieve details of a selected record
- Automatic database setup on first run
- SQLite fallback for environments without MySQL installed

## Folder Contents

- `onlinestudy.py` – main Python application and GUI logic
- `onlinestudy.sql` – SQL schema and database setup script
- `pract1.sql` – additional database practice script
- `.gitignore` – ignores generated files and local caches

## Requirements

- Python 3.8 or later
- Tkinter (usually included with Python on Windows/macOS)

## Run the Project

From the project folder, run:

```bash
python onlinestudy.py
```

## Database Behavior

The app automatically creates and initializes the required SQLite database file locally in the project folder.

## Notes

- The project was originally designed around MySQL, but it now falls back to SQLite when MySQL is unavailable, making it easier to run locally.
- The SQL scripts are included for reference and schema understanding.

## License

This project is intended for academic and educational use.
