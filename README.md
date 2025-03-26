# Library Management System

A simple Python-based application for managing a library's books and students. The system allows you to add and search for books, register students, check books in and out, collect fees, and remove students. Data is stored in CSV files for persistence.

## Features

- **Add Book:** Add a new book to the library.
- **Add Student:** Register a new student.
- **Check Out Book:** Allow students to borrow books.
- **Return Book:** Process the return of a borrowed book.
- **List Available Books:** Display all books that are not currently checked out.
- **Collect Fees:** Apply fees for students with more than three checked-out books.
- **Remove Student:** Delete a student's record.
- **Search Book:** Search for books by title or author.

## How to Run

1. **Requirements:**  
   - Python 3.6 or later  
   - Write permissions in the working directory (for creating/updating CSV files)

2. **Execution:**  
   Run the application with:
   ```bash
   python <script_name>.py
   ```
   Replace `<script_name>.py` with the name of your Python file.

3. **Usage:**  
   Follow the on-screen menu to navigate the system. Data will load automatically on startup and save when you exit the program.

## Data Storage

- **Books Data:** Stored in `books.csv`
- **Students Data:** Stored in `students.csv`

Data is read from and written to these files, ensuring that your library records persist across sessions.

---

This project is straightforward and easy to use, making it a great starting point for building more advanced library management solutions. Enjoy managing your library!
