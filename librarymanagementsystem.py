from datetime import datetime as dt  # using 'as' for aliasing, datetime is imported as 'dt'
import os  # 'import' brings in the os module

library_name = "Library Management System"

# Global variables to store the data for all books and students.
ALL_BOOKS = []  # A list to store all Book objects.
ALL_STUDENTS = []  # A list to store all Student objects.

# 'class' keyword defines a new user-defined class.
class Book:
    """A Book with title, author, and checkout tracking."""
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_checked_out = False
        self.due_date = None

class Student:
    """A Student that can borrow books."""
    next_id = 1
    def __init__(self, name):
        self.student_id = Student.next_id
        Student.next_id += 1
        self.name = name
        self.checked_out_books = []
        self.fees = 0.0

# Define a function to load existing data.
def load_data():
    """Load existing data from CSV files if they exist."""
    # 'global' allows modification of global variables within this function.
    global ALL_BOOKS, ALL_STUDENTS

    # Check if the books CSV file exists; 'if' condition.
    if not os.path.exists("books.csv"):
        print("No existing books.csv found.")
    else:
        # 'with' ensures the file is properly closed after processing.
        with open("books.csv", "r") as bf:
            for line in bf:  # 'for' loop iterates over each line in the file.
                line = line.strip()
                if line:  # 'if' condition checks for non-empty line.
                    # Splitting CSV data.
                    title, author, is_out, due_str = line.split(",")
                    bk = Book(title, author)

                    # Setting book checkout status; 'is_out.lower() == "true"' uses 'not' implicitly.
                    bk.is_checked_out = (is_out.lower() == "true")
                    
                    # Convert 'None' string back to actual None.
                    bk.due_date = due_str if due_str != "None" else None
                    ALL_BOOKS.append(bk)


    if not os.path.exists("students.csv"):
        print("No existing students.csv found.")
    else:
        with open("students.csv", "r") as pf:
            for line in pf:
                line = line.strip()
                if line:
                    parts = line.split(",")  # name, fees, [books...]
                    s = Student(parts[0])
                    s.fees = float(parts[1])
                    if len(parts) > 2:
                        # 'for' loop to iterate over book titles.
                        book_titles = parts[2:]
                        for bt in book_titles:
                            for stored_book in ALL_BOOKS:
                                # Compare titles ignoring case.
                                if stored_book.title == bt:
                                    s.checked_out_books.append(stored_book)
                    ALL_STUDENTS.append(s)

def save_data():
    """Save data to CSV using 'try', 'except', 'finally'."""
    try:
        # Writing book data.
        with open("books.csv", "w") as bf:
            for bk in ALL_BOOKS:
                bf.write(f"{bk.title},{bk.author},{bk.is_checked_out},{bk.due_date}\n")

        # Writing student data.
        with open("students.csv", "w") as pf:
            for stu in ALL_STUDENTS:
                # List comprehension to collect titles from checked-out books.
                borrowed_titles = [b.title for b in stu.checked_out_books]
                line = f"{stu.name},{stu.fees}"
                if borrowed_titles:
                    line += "," + ",".join(borrowed_titles)
                pf.write(line + "\n")

    except OSError as e:  # 'except' handles exceptions that occur in the try block.
        print("Error saving data:", e)
        raise  # 'raise' re-raises the caught exception.
    finally:
        # 'finally' always executes, whether an exception occurred or not.
        print("Data save operation finished.")

def add_book(title, author):
    """Add a Book to the global library data."""
    global ALL_BOOKS  # 'global' used to modify the global ALL_BOOKS list.
    new_book = Book(title, author)
    ALL_BOOKS.append(new_book)
    return new_book  # 'return' exits the function and outputs new_book.

def find_student(name):
    """Return a matching student or None using lambda."""
    # 'lambda' creates an anonymous function to compare student names.
    results = list(filter(lambda s: s.name.lower() == name.lower(), ALL_STUDENTS))
    if results:
        return results[0]
    return None

def remove_student(name):
    """Remove a student using 'del' if found."""
    global ALL_STUDENTS
    s = find_student(name)
    if s:
        # 'del' removes an element from a list by index.
        del ALL_STUDENTS[ALL_STUDENTS.index(s)]
        return f"Student '{s.name}' removed successfully."
    return "Student not found."

def add_student(name):
    """Add a student if not already existing."""
    existing = find_student(name)
    # 'is not None' checks that a value exists.
    if existing is not None:
        return existing
    new_s = Student(name)
    ALL_STUDENTS.append(new_s)
    return new_s

def yield_books(only_available=False):
    """Generate books using 'yield'."""
    for bk in ALL_BOOKS:  # 'for' iterates through ALL_BOOKS.
        if only_available and bk.is_checked_out:
            continue  # 'continue' skips to the next iteration if condition is met.
        yield bk  # 'yield' pauses the function and returns a book.

def check_out_book(student, book_title):
    """Student checks out a book, if available."""
    for bk in yield_books():
        # 'if' checks if the title matches and the book is not already checked out.
        if bk.title.lower() == book_title.lower() and not bk.is_checked_out:
            bk.is_checked_out = True
            # Set due date using dt (current date formatted).
            bk.due_date = dt.now().strftime("%Y-%m-%d")
            student.checked_out_books.append(bk)
            return f"'{bk.title}' checked out by {student.name}."
    # 'else' of the for-loop is implicit here by returning outside the loop.
    return f"No available copy of '{book_title}' found."

def return_book(student, book_title):
    """Return a Book that was checked out by Student."""
    for bk in student.checked_out_books:
        if bk.title.lower() == book_title.lower():
            bk.is_checked_out = False
            bk.due_date = None
            # Remove the book from the student's list.
            student.checked_out_books.remove(bk)
            return f"'{book_title}' returned by {student.name}."
    return f"{student.name} does not have '{book_title}' checked out."

def collect_fees():
    """Demonstrate 'assert', 'nonlocal', 'pass' in a nested function."""
    total_collected = 0.0
    # Nested function to apply fee to a student.
    def apply_fee(student):
        nonlocal total_collected  # 'nonlocal' allows modifying the outer variable.
        if len(student.checked_out_books) > 3:
            student.fees += 5.0
            total_collected += 5.0
        else:
            pass  # 'pass' is a placeholder that does nothing.
    for stu in ALL_STUDENTS:
        apply_fee(stu)
    # 'assert' is used here to ensure that total_collected is not negative.
    assert total_collected >= 0, "Total collected fees cannot be negative!"
    return total_collected


def search_book(query):
    """
    Search for books by title or author. Returns a list of matching books.
    """
    query = query.lower()
    results = []
    for bk in ALL_BOOKS:
        if query in bk.title.lower() or query in bk.author.lower():
            results.append(bk)
    return results

def main():
    load_data()  # Load data from CSV files.
    # 'while' creates a loop that continues until a break condition is met.
    while True:
        # Displaying the menu.
        print("\n" + "="*40)
        print(f"{library_name:^40}")  # Center the title in a 40-character width
        print("="*40)
        print("1) Add Book")
        print("2) Add Student")
        print("3) Check Out Book")
        print("4) Return Book")
        print("5) List Available Books")
        print("6) Collect Fees")
        print("7) Remove Student")
        print("8) Search Book")
        print("Q) Quit")
        print("="*40)

        choice = input("Select an option: ")

        if choice == "1":
            t = input("Enter book title: ")
            a = input("Enter book author: ")
            bk = add_book(t, a)
            print(f"Book '{bk.title}' by {bk.author} has been added successfully!")
        elif choice == "2":  # 'elif' is short for 'else if'
            name = input("Enter student name: ")
            stu = add_student(name)
            print(f"Student '{stu.name}' added or retrieved.")
        elif choice == "3":
            name = input("Enter student name: ")
            stu = find_student(name)
            if stu is None:  # Check if student was not found.
                print("Student not found. Please add the student first.")
                continue  # 'continue' skips the rest of the loop and starts the next iteration.
            book_title = input("Enter book title to check out: ")
            msg = check_out_book(stu, book_title)
            print(msg)
        elif choice == "4":
            name = input("Enter student name: ")
            stu = find_student(name)
            if stu is None:
                print("Student not found.")
                continue
            book_title = input("Enter book title to return: ")
            msg = return_book(stu, book_title)
            print(msg)
        elif choice == "5":
            print("Available Books:")
            for b in yield_books(only_available=True):  # 'for' loop iterates over available books.
                print(f"- {b.title} by {b.author}")
        elif choice == "6":
            collected = collect_fees()
            print(f"Total fees collected: ${collected}")
        elif choice == "7":
            name = input("Enter the student name to remove: ")
            msg = remove_student(name)
            print(msg)
        elif choice == "8":
            query = input("Enter a title or author to search: ")
            matches = search_book(query)
            if matches:
                print("Search Results:")
                for bk in matches:
                    status = "Available" if not bk.is_checked_out else "Checked Out"
                    print(f"- {bk.title} by {bk.author} [{status}]")
            else:
                print("No books matched your search query.")
        elif choice.lower() == "q":
            print("Saving data and exiting...")
            save_data()
            break  # 'break' exits the while loop.
        else:
            print("Invalid choice. Please try again.")

# 'if __name__ == "__main__":' ensures that main() is called only when this script is run directly.
if __name__ == "__main__":
    main()