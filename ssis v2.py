import tkinter as tk
import mysql.connector

# Establish a connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Iamachampion123yeah",
    database="SSIS_v2"
)
cursor = db.cursor()

def main_menu():
    # Create the main menu window
    window = tk.Tk()
    window.title("Main Menu")
    window.geometry ('600x400')

    # Create menu buttons
    student_button = tk.Button(window, text="Student Data", command=student_menu)
    student_button.pack()

    course_button = tk.Button(window, text="Course Data", command=course_menu)
    course_button.pack()

    # Start the main loop
    window.mainloop()

def student_menu():
    # Create the student menu window
    window = tk.Tk()
    window.title("Student Menu")
    window.geometry ('600x400')

    # Create menu buttons
    write_button = tk.Button(window, text="Write Student Data", command=write_student_data)
    write_button.pack()

    list_button = tk.Button(window, text="List Student Data", command=list_student_data)
    list_button.pack()

    edit_button = tk.Button(window, text="Edit Student Data", command=edit_student_data)
    edit_button.pack()

    delete_button = tk.Button(window, text="Delete Student Data", command=delete_student_data)
    delete_button.pack()

    search_year_button = tk.Button(window, text="Search Student by Year", command=search_student_year)
    search_year_button.pack()

    search_name_button = tk.Button(window, text="Search Student by Name", command=search_student_name)
    search_name_button.pack()

    back_button = tk.Button(window, text="Back to Main Menu", command=window.destroy)
    back_button.pack()

def write_student_data():
    # Create a new student record
    id_number = input("\nEnter ID Number (or 'q' to quit): ")
    if id_number == 'q':
        return

    if is_student_exists(id_number):
        print("This student already exists.")
        return

    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    gender = input("Enter Gender: ")
    year = input("Enter Year: ")
    course = input("Enter Course Name: ")

    # Insert the student record into the database
    query = "INSERT INTO students (id_number, first_name, last_name, gender, year, course) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (id_number, first_name, last_name, gender, year, course)
    cursor.execute(query, values)
    db.commit()

    print("\nStudent Data written successfully.")

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
    for row in result:
        print(row)
    print("\nStudent Data listed successfully.")

def edit_student_data():
    # Update an existing student record in the database
    id_number = input("\nEnter ID Number to edit (or 'q' to quit): ")
    if id_number == 'q':
        return

    if not is_student_exists(id_number):
        print("Student not found.")
        return

    first_name = input("Enter new First Name: ")
    last_name = input("Enter new Last Name: ")
    gender = input("Enter new Gender: ")
    year = input("Enter new Year: ")
    course = input("Enter new Course: ")

    query = "UPDATE students SET first_name = %s, last_name = %s, gender = %s, year = %s, course = %s WHERE id_number = %s"
    values = (first_name, last_name, gender, year, course, id_number)
    cursor.execute(query, values)
    db.commit()

    print("Student data updated successfully.")

def delete_student_data():
    # Delete an existing student record from the database
    id_number = input("\nEnter ID Number to delete (or 'q' to quit): ")
    if id_number == 'q':
        return

    if not is_student_exists(id_number):
        print("Student not found.")
        return

    query = "DELETE FROM students WHERE id_number = %s"
    cursor.execute(query, (id_number,))
    db.commit()

    print("Student data deleted successfully.")

def search_student_year():
    # Search for students by year
    year = input("\nEnter the Year of student (or 'q' to quit): ")
    if year == 'q':
        return

    query = "SELECT * FROM students WHERE year = %s"
    cursor.execute(query, (year,))
    result = cursor.fetchall()

    if result:
        for row in result:
            print(row)
    else:
        print("Student does not exist.")

def search_student_name():
    # Search for students by name
    name = input("\nEnter the first name of student (or 'q' to quit): ")
    if name == 'q':
        return

    query = "SELECT * FROM students WHERE first_name LIKE %s OR last_name LIKE %s"
    cursor.execute(query, (f"%{name}%", f"%{name}%"))
    result = cursor.fetchall()

    if result:
        for row in result:
            print(row)
    else:
        print("Student does not exist.")

def course_menu():
    # Create the course menu window
    window = tk.Tk()
    window.title("Course Menu")
    window.geometry ('600x400')

    # Create menu buttons
    write_button = tk.Button(window, text="Write Course Data", command=write_course_data)
    write_button.pack()

    list_button = tk.Button(window, text="List Course Data", command=list_course_data)
    list_button.pack()

    edit_button = tk.Button(window, text="Edit Course Data", command=edit_course_data)
    edit_button.pack()

    delete_button = tk.Button(window, text="Delete Course Data", command=delete_course_data)
    delete_button.pack()

    search_button = tk.Button(window, text="Search Course", command=search_courses)
    search_button.pack()

    back_button = tk.Button(window, text="Back to Main Menu", command=window.destroy)
    back_button.pack()

def write_course_data():
    # Create a new course record
    course_name = input("\nEnter Course Name (or 'q' to quit): ")
    if course_name == 'q':
        return

    if does_course_exists(course_name):
        print("This course already exists.")
        return

    course_code = input("Enter Course Code: ")
    college = input("Enter College: ")

    # Insert the course record into the database
    query = "INSERT INTO courses (course_name, course_code, college) VALUES (%s, %s, %s)"
    values = (course_name, course_code, college)
    cursor.execute(query, values)
    db.commit()

    print("\nCourse Data written successfully.")

def does_course_exists(course_name):
    # Check if the course record already exists in the database
    query = "SELECT course_name FROM courses WHERE course_name = %s"
    cursor.execute(query, (course_name,))
    result = cursor.fetchone()
    return result is not None

def list_course_data():
    # Retrieve and display all course records from the database
    query = "SELECT * FROM courses"
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        print(row)
    print("\nCourse Data listed successfully.")

def edit_course_data():
    # Update an existing course record in the database
    course_name = input("\nEnter Course Name to edit (or 'q' to quit): ")
    if course_name == 'q':
        return

    if not does_course_exists(course_name):
        print("Course not found.")
        return

    course_code = input("Enter new Course Code: ")
    college = input("Enter new College: ")

    query = "UPDATE courses SET course_code = %s, college = %s WHERE course_name = %s"
    values = (course_code, college, course_name)
    cursor.execute(query, values)
    db.commit()

    print("Course data updated successfully.")

def delete_course_data():
    # Delete an existing course record from the database
    course_name = input("\nEnter Course Name to delete (or 'q' to quit): ")
    if course_name == 'q':
        return

    if not does_course_exists(course_name):
        print("Course not found.")
        return

    query = "DELETE FROM courses WHERE course_name = %s"
    cursor.execute(query, (course_name,))
    db.commit()

    print("Course data deleted successfully.")

def search_courses():
    # Search for courses
    keyword = input("\nEnter a keyword to search for courses (or 'q' to quit): ")
    if keyword == 'q':
        return

    query = "SELECT * FROM courses WHERE course_name LIKE %s OR course_code LIKE %s OR college LIKE %s"
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    result = cursor.fetchall()

    if result:
        for row in result:
            print(row)
    else:
        print("Course does not exist.")

# Start the program
main_menu()

# Close the database connection
db.close()
