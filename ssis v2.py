import tkinter as tk
from tkinter import simpledialog, messagebox
import mysql.connector

# Establish a connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your password",
    database="your database"
)
cursor = db.cursor()

# Declare window as a global variable
window = None

def show_message(title, message):
    # Show a message dialog
    messagebox.showinfo(title, message)

def main_menu():
    global window
    # Create the main menu window
    window = tk.Tk()
    window.title("Main Menu")
    window.geometry('300x200')

    # Create menu buttons
    student_button = tk.Button(window, text="Student", command=student_menu, width=20, height=2)
    student_button.pack()

    course_button = tk.Button(window, text="Course", command=course_menu, width=20, height=2)
    course_button.pack()

    # Start the main loop
    window.mainloop()

def student_menu():
    # Create the student menu window
    student_window = tk.Toplevel(window)
    student_window.title("Student Menu")
    student_window.geometry('600x300')

    # Create menu buttons with icons and tooltips
    write_button = tk.Button(student_window, text="Write Student Data", command=write_student_data, width=20, height=2)
    write_button.pack()

    list_button = tk.Button(student_window, text="List Student Data", command=list_student_data, width=20, height=2)
    list_button.pack()

    edit_button = tk.Button(student_window, text="Edit Student Data", command=edit_student_data, width=20, height=2)
    edit_button.pack()

    delete_button = tk.Button(student_window, text="Delete Student Data", command=delete_student_data, width=20, height=2)
    delete_button.pack()

    search_button = tk.Button(student_window, text="Search Student", command=search_students, width=20, height=2)
    search_button.pack()

    back_button = tk.Button(student_window, text="Back to Main Menu", command=student_window.destroy, width=20, height=2)
    back_button.pack()

def show_data(title, data):
    # Display data in a new window using a Listbox widget with scrollbars
    data_window = tk.Toplevel(window)
    data_window.title(title)

    listbox = tk.Listbox(data_window, width=100, height=20)
    listbox.pack()

    scrollbar = tk.Scrollbar(data_window, command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    for row in data:
        listbox.insert(tk.END, str(row))

def get_input(prompt):
    # Get user input using a dialog window
    user_input = simpledialog.askstring("Input", prompt)
    return user_input

def write_student_data():
    # Create a new student record
    id_number = get_input("Enter ID Number (or 'q' to quit): ")
    if id_number == 'q':
        return

    if is_student_exists(id_number):
        messagebox.showerror("Error", "This student already exists.")
        return

    first_name = get_input("Enter First Name:")
    if not first_name:
        return

    last_name = get_input("Enter Last Name:")
    if not last_name:
        return

    gender = get_input("Enter Gender:")
    if not gender:
        return

    year_level = get_input("Enter Year:")
    if not year_level:
        return

    course = get_input("Enter Course Name:")
    if not course:
        return

    # Add a dash to the id_number before inserting into the database
    id_number_with_dash = id_number[:4] + '-' + id_number[4:]

    # Insert the student record into the database
    query = "INSERT INTO students (id_number, first_name, last_name, gender, year_level, course) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (id_number_with_dash, first_name, last_name, gender, year_level, course)
    cursor.execute(query, values)
    db.commit()

    messagebox.showinfo("Success", "Student Data written successfully.")

def is_student_exists(id_number):
    # Check if the student record already exists in the database
    query = "SELECT id_number FROM students WHERE id_number = %s"
    cursor.execute(query, (id_number,))
    result = cursor.fetchone()
    return result is not None

def list_student_data():
    # Retrieve and display all student records from the database
    query = "SELECT * FROM students"
    cursor.execute(query)
    result = cursor.fetchall()

    # Exclude rows with a None value in the first column (assuming it is the ID column)
    temp_result = []
    for item in result:
        if item[1] is not None:
            temp_result.append(item[1:])

    show_data("Student Data", temp_result)

def edit_student_data():
    # Update an existing student record in the database
    id_number = get_input("Enter ID Number to edit (or 'q' to quit): ")
    if id_number is None or id_number.strip().lower() == 'q':
        return

    if not is_student_exists(id_number):
        show_message("Error", "Student not found.")
        return

    first_name = get_input("Enter new First Name: ")
    last_name = get_input("Enter new Last Name: ")
    gender = get_input("Enter new Gender: ")
    year = get_input("Enter new Year: ")
    course = get_input("Enter new Course: ")

    query = "UPDATE students SET first_name = %s, last_name = %s, gender = %s, year_level = %s, course = %s WHERE id_number = %s"
    values = (first_name, last_name, gender, year, course, id_number)
    cursor.execute(query, values)
    db.commit()

    show_message("Success", "Student data updated successfully.")

def delete_student_data():
    # Delete an existing student record from the database
    id_number = get_input("Enter ID Number to delete (or 'q' to quit): ")
    if id_number is None or id_number.strip().lower() == 'q':
        return

    if not is_student_exists(id_number):
        show_message("Error", "Student not found.")
        return

    # Confirm before deleting the student data
    if not get_confirmation("Are you sure you want to delete this student?"):
        return

    query = "DELETE FROM students WHERE id_number = %s"
    cursor.execute(query, (id_number,))
    db.commit()

    show_message("Success", "Student data deleted successfully.")

def search_students():
    search_option = get_input("Choose and enter search keyword (ID, Name, Year, Gender, Course): ")
    if search_option is None or search_option.strip().lower() == 'q':
        return

    query = ""
    values = ()
    result = None

    if search_option.lower() == 'id':
        id_number = get_input("Enter the ID Number of student: ")
        if id_number is None:
            return
        query = "SELECT * FROM students WHERE id_number = %s"
        values = (id_number,)
    elif search_option.lower() == 'name':
        name = get_input("Enter the first name of student: ")
        if name is None:
            return
        query = "SELECT * FROM students WHERE first_name LIKE %s OR last_name LIKE %s"
        values = (f"%{name}%", f"%{name}%")
    elif search_option.lower() == 'year':
        year = get_input("Enter the Year of student: ")
        if year is None:
            return
        query = "SELECT * FROM students WHERE year_level = %s"
        values = (year,)
    elif search_option.lower() == 'gender':
        gender = get_input("Enter the Gender of student: ")
        if gender is None:
            return
        query = "SELECT * FROM students WHERE gender = %s"
        values = (gender,)
    elif search_option.lower() == 'course':
        course = get_input("Enter the Course of student: ")
        if course is None:
            return
        query = "SELECT * FROM students WHERE course LIKE %s"
        values = (f"%{course}%",)

    cursor.execute(query, values)
    result = cursor.fetchall()

    if not result:  # Check if the result is empty
        show_message("Search Result", "No matching records found.")
        return

    # Exclude the id from each row in the result
    temp_result = []
    for item in result:
        temp_result.append(item[1:])

    show_data("Search Results", temp_result)

def course_menu():
    # Create the course menu window
    course_window = tk.Toplevel(window)
    course_window.title("Course Menu")
    course_window.geometry('600x400')

    # Create menu buttons with icons and tooltips
    write_button = tk.Button(course_window, text="Write Course Data", command=write_course_data, width=20, height=2)
    write_button.pack()

    list_button = tk.Button(course_window, text="List Course Data", command=list_course_data, width=20, height=2)
    list_button.pack()

    edit_button = tk.Button(course_window, text="Edit Course Data", command=edit_course_data, width=20, height=2)
    edit_button.pack()

    delete_button = tk.Button(course_window, text="Delete Course Data", command=delete_course_data, width=20, height=2)
    delete_button.pack()

    search_button = tk.Button(course_window, text="Search Course", command=search_courses, width=20, height=2)
    search_button.pack()

    back_button = tk.Button(course_window, text="Back to Main Menu", command=course_window.destroy, width=20, height=2)
    back_button.pack()

def write_course_data():
    # Create a new course record
    course_name = get_input("Enter Course Name:")
    if course_name is None:
        return

    if does_course_exists(course_name):
        show_message("Error", "This course already exists.")
        return

    course_code = get_input("Enter Course Code:")
    if course_code is None:
        return

    college = get_input("Enter College:")
    if college is None:
        return

    # Confirm before inserting the course data
    if not get_confirmation("Are you sure you want to add this course?"):
        return

    # Insert the course record into the database
    query = "INSERT INTO courses (course_name, course_code, college) VALUES (%s, %s, %s)"
    values = (course_name, course_code, college)
    cursor.execute(query, values)
    db.commit()

    show_message("Success", "Course data written successfully.")

def does_course_exists(course_name):
    # Check if the course record already exists in the database
    query = "SELECT course_name FROM courses WHERE course_name = %s"
    cursor.execute(query, (course_name,))
    result = cursor.fetchone()

    print("Course exists in database:", result)  # Debug print

    return result is not None

def list_course_data():
    # Retrieve and display all course records from the database
    query = "SELECT * FROM courses"
    cursor.execute(query)
    result = cursor.fetchall()

    # Exclude the id from each row in the result
    temp_result = []
    for item in result:
        temp_result.append(item[1:])

    show_data("Course Data", temp_result)

def edit_course_data():
    # Update an existing course record in the database
    course_code = get_input("Enter Course Code to edit (or 'q' to quit): ")
    if course_code is None or course_code.strip().lower() == 'q':
        return

    if not does_course_exists(course_code):
        show_message("Error", "Course not found.")
        return

    new_course_code = get_input("Enter new Course Code: ")
    college = get_input("Enter new College: ")

    query = "UPDATE courses SET course_code = %s, college = %s WHERE course_code = %s"
    values = (new_course_code, college, course_code)
    cursor.execute(query, values)
    db.commit()

    show_message("Success", "Course data updated successfully.")

def delete_course_data():
    # Delete an existing course record from the database
    course_name = get_input("Enter Course Name to delete (or 'q' to quit): ")
    if course_name is None or course_name.strip().lower() == 'q':
        return

    print("Deleting course:", course_name)  # Debug print

    if not does_course_exists(course_name):
        print("Course not found in database.")  # Debug print
        show_message("Error", "Course not found.")
        return

    # Confirm before deleting the course data
    if not get_confirmation("Are you sure you want to delete this course?"):
        return

    query = "DELETE FROM courses WHERE course_name = %s"
    cursor.execute(query, (course_name,))
    db.commit()

    show_message("Success", "Course data deleted successfully.")

def search_courses():
    # Search for courses
    keyword = get_input("Enter a keyword to search for courses (or 'q' to quit): ")
    if keyword is None or keyword.strip().lower() == 'q':
        return

    query = "SELECT * FROM courses WHERE course_name LIKE %s OR course_code LIKE %s OR college LIKE %s"
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    result = cursor.fetchall()

    if result:
        show_data("Search Results", result)
    else:
        show_message("Search Result", "Course does not exist.")

def get_confirmation(message):
    # Show a confirmation dialog with Yes/No options
    result = messagebox.askyesno("Confirmation", message)
    return result

# Start the program
main_menu()

# Close the database connection
db.close()
