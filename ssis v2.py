import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import mysql.connector

# Establish a connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Iamachampion123yeah",
    database="SSIS_v2"
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

def create_menu_window(title, width, height):
    menu_window = tk.Toplevel(window)
    menu_window.title(title)
    menu_window.geometry(f'{width}x{height}')
    return menu_window

def create_labeled_combobox(parent, label_text, values, default_value):
    label = tk.Label(parent, text=label_text)
    label.pack()

    variable = tk.StringVar()
    variable.set(default_value)

    combobox = ttk.Combobox(parent, textvariable=variable, values=values)
    combobox.pack()

    return variable

def write_student_data():
    # Get student's details
    id_number = get_input("Enter ID Number (or 'q' to quit): ")
    if id_number == 'q':
        return

    if is_student_exists(id_number):
        show_message("Error", "This student already exists.")
        return

    first_name = get_input("Enter First Name:")
    if not first_name:
        return

    last_name = get_input("Enter Last Name:")
    if not last_name:
        return

    gender_options = ["Male", "Female"]
    course_options = get_course_options()

    student_window = create_menu_window("Write Student Data", 400, 300)

    gender_var = create_labeled_combobox(student_window, "Select Gender:", gender_options, gender_options[0])
    course_var = create_labeled_combobox(student_window, "Select Course:", course_options, course_options[0])

    year_level = get_input("Enter Year:")
    if not year_level:
        return

    id_number_with_dash = insert_dash_to_id(id_number)

    def save_student():
        if is_student_exists(id_number_with_dash):
            show_message("Error", "This student already exists.")
            return

        if insert_student_record(id_number_with_dash, first_name, last_name, gender_var.get(), year_level, course_var.get()):
            show_message("Success", "Student Data written successfully.")
            student_window.destroy()

    save_button = tk.Button(student_window, text="Save", command=save_student)
    save_button.pack()

def insert_dash_to_id(id_number):
    return id_number[:4] + '-' + id_number[4:]

def get_course_options():
    courses_query = "SELECT course_name FROM courses"
    cursor.execute(courses_query)
    courses = cursor.fetchall()
    return [course[0] for course in courses]

def is_student_exists(id_number):
    query = "SELECT id_number FROM students WHERE id_number = %s"
    cursor.execute(query, (id_number,))
    result = cursor.fetchone()
    return result is not None

def insert_student_record(id_number, first_name, last_name, gender, year_level, course):
    try:
        query = "INSERT INTO students (id_number, first_name, last_name, gender, year_level, course) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (id_number, first_name, last_name, gender, year_level, course)
        cursor.execute(query, values)
        db.commit()
        return True
    except mysql.connector.Error as e:
        show_message("Error", f"An error occurred while writing student data: {e}")
        return False

def list_student_data():
    # Retrieve and display all student records from the database
    query = "SELECT id_number, first_name, last_name, gender, year_level, course FROM students"
    cursor.execute(query)
    result = cursor.fetchall()

    show_data("Student Data", result)

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
    try:
        # Delete an existing student record from the database
        id_number = get_input("Enter ID Number to delete (or 'q' to quit): ")
        if id_number is None or id_number.strip().lower() == 'q':
            return

        if not is_student_exists(id_number):
            show_message("Error", "Student not found.")
            return

        # Confirm before deleting the student data
        confirmation = get_confirmation("Are you sure you want to delete this student?")
        if not confirmation:
            return

        query = "DELETE FROM students WHERE id_number = %s"
        cursor.execute(query, (id_number,))
        db.commit()

        show_message("Success", "Student data deleted successfully.")
    except mysql.connector.Error as e:
        show_message("Error", f"An error occurred while deleting student data: {e}")

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
        query = "SELECT id_number, first_name, last_name, gender, year_level, course FROM students WHERE id_number = %s"
        values = (id_number,)
    elif search_option.lower() == 'name':
        name = get_input("Enter the first name of student: ")
        if name is None:
            return
        query = "SELECT id_number, first_name, last_name, gender, year_level, course FROM students WHERE first_name LIKE %s OR last_name LIKE %s"
        values = (f"%{name}%", f"%{name}%")
    elif search_option.lower() == 'year':
        year = get_input("Enter the Year of student: ")
        if year is None:
            return
        query = "SELECT id_number, first_name, last_name, gender, year_level, course FROM students WHERE year_level = %s"
        values = (year,)
    elif search_option.lower() == 'gender':
        gender = get_input("Enter the Gender of student: ")
        if gender is None:
            return
        query = "SELECT id_number, first_name, last_name, gender, year_level, course FROM students WHERE gender = %s"
        values = (gender,)
    elif search_option.lower() == 'course':
        course = get_input("Enter the Course of student: ")
        if course is None:
            return
        query = "SELECT id_number, first_name, last_name, gender, year_level, course FROM students WHERE course LIKE %s"
        values = (f"%{course}%",)

    cursor.execute(query, values)
    result = cursor.fetchall()

    if not result:  # Check if the result is empty
        show_message("Search Result", "No matching records found.")
        return

    show_data("Search Results", result)

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

    # Clear entry fields
    course_name_entry.delete(0, tk.END)
    course_code_entry.delete(0, tk.END)
    college_entry.delete(0, tk.END)

    # Optional: Update course options in course_combobox
    update_course_combobox()

def update_course_combobox():
    # Update course options in the course_combobox
    courses_query = "SELECT course_name FROM courses"
    cursor.execute(courses_query)
    courses = cursor.fetchall()
    course_options = [course[0] for course in courses]
    course_combobox['values'] = course_options
    course_combobox.set(course_options[0])  # Reset the selected value

    # Insert the course record into the database
    query = "INSERT INTO courses (course_name, course_code, college) VALUES (%s, %s, %s)"
    values = (course_name, course_code, college)
    cursor.execute(query, values)
    db.commit()

    show_message("Success", "Course data written successfully.")
    
    # Clear entry fields
    course_name_entry.delete(0, tk.END)
    course_code_entry.delete(0, tk.END)
    college_entry.delete(0, tk.END)

def does_course_exists(course_name):
    # Check if the course record already exists in the database
    query = "SELECT course_name FROM courses WHERE LOWER(course_name) = %s"
    cursor.execute(query, (course_name.lower(),))
    result = cursor.fetchone()

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

    cursor.fetchall()

    show_data("Course Data", temp_result)

def edit_course_data():
    # Update an existing course record in the database
    course_name = get_input("Enter Course Name to edit (or 'q' to quit): ")

    if course_name is None or course_name.strip().lower() == 'q':
        return

    if not does_course_exists(course_name):
        show_message("Error", "Course not found.")
        return

    new_course_name = get_input("Enter new Course Name (leave blank to keep current): ")

    new_course_code = get_input("Enter new Course Code (leave blank to keep current): ")

    new_college = get_input("Enter new College (leave blank to keep current): ")

    # Construct the update query based on user input
    update_query = "UPDATE courses SET"
    update_values = []

    if new_course_name:
        update_query += " course_name = %s,"
        update_values.append(new_course_name)

    if new_course_code:
        update_query += " course_code = %s,"
        update_values.append(new_course_code)

    if new_college:
        update_query += " college = %s,"
        update_values.append(new_college)

    # Remove trailing comma from query if necessary
    if update_query.endswith(","):
        update_query = update_query[:-1]

    update_query += " WHERE course_name = %s"
    update_values.append(course_name)

    if not update_values:
        show_message("No Changes", "No changes made.")
        return

    cursor.execute(update_query, update_values)
    db.commit()

    # Update students' course in case course name was changed
    if new_course_name:
        update_students_course(course_name, new_course_name)

    show_message("Success", "Course data updated successfully.")

def update_students_course(old_course_name, new_course_name):
    # Update students' course in the database
    query = "UPDATE students SET course = %s WHERE course = %s"
    cursor.execute(query, (new_course_name, old_course_name))
    db.commit()

def delete_course_data():
    # Delete an existing course record from the database
    course_name = get_input("Enter Course Name to delete (or 'q' to quit): ")
    if course_name is None or course_name.strip().lower() == 'q':
        return

    if not does_course_exists(course_name):
        show_message("Error", "Course not found.")
        return

    # Confirm before deleting the course data
    if not get_confirmation("Are you sure you want to delete this course?"):
        return

    # Delete students associated with the course
    delete_students_with_course(course_name)

    # Delete the course record
    query = "DELETE FROM courses WHERE course_name = %s"
    cursor.execute(query, (course_name,))
    db.commit()

    show_message("Success", "Course data deleted successfully.")

def delete_students_with_course(course_name):
    # Delete students with the specified course
    query = "DELETE FROM students WHERE course = %s"
    cursor.execute(query, (course_name,))
    db.commit()

def search_courses():
    # Search for courses
    keyword = get_input("Enter a keyword to search for courses (or 'q' to quit): ")
    if keyword is None or keyword.strip().lower() == 'q':
        return

    query = "SELECT course_name, course_code, college FROM courses WHERE course_name LIKE %s OR course_code LIKE %s OR college LIKE %s"
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