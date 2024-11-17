import customtkinter as ctk
from tkinter import messagebox, simpledialog, ttk
from db_cn import execute_query

def load_employees():
    # Clear the table first
    for row in employee_tree.get_children():
        employee_tree.delete(row)

    # Fetch all employee data
    query = "SELECT emp_id, emp_name, role, age, gender, email, mobile, address FROM employees"
    results = execute_query(query)

    # Insert data into the table
    for row in results:
        employee_tree.insert("", "end", values=row)

def open_insert_window():
    def insert_employee():
        emp_name = emp_name_var.get()
        role = role_var.get()
        age = age_var.get()
        gender = gender_var.get()
        email = email_var.get()
        mobile = mobile_var.get()
        address = address_var.get()
        password = "Changeme@123"  # Default password

        # Insert employee into the employees table
        query = """
        INSERT INTO employees (emp_name, role, age, gender, email, mobile, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (emp_name, role, age, gender, email, mobile, address)
        execute_query(query, params)

        result = execute_query("SELECT emp_id from employees WHERE emp_name = %s", (emp_name,))

        emp_id = result[0][0]
        query = "INSERT INTO employee_credentials(emp_id, role, password) VALUES (%s, %s, %s)"
        params = (emp_id, role, password)
        execute_query(query, params)

        load_employees()  # Refresh the employee list
        insert_window.destroy()  # Close the insert window

    insert_window = ctk.CTkToplevel()
    insert_window.title("Insert Employee")

    emp_name_var = ctk.StringVar()
    role_var = ctk.StringVar()
    age_var = ctk.IntVar()
    gender_var = ctk.StringVar()
    email_var = ctk.StringVar()
    mobile_var = ctk.StringVar()
    address_var = ctk.StringVar()

    # Using grid layout for better organization with prefixes
    ctk.CTkLabel(insert_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    ctk.CTkEntry(insert_window, textvariable=emp_name_var).grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(insert_window, text="Role:").grid(row=1, column=0, padx=5, pady=5)
    ctk.CTkEntry(insert_window, textvariable=role_var).grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(insert_window, text="Age:").grid(row=2, column=0, padx=5, pady=5)
    ctk.CTkEntry(insert_window, textvariable=age_var).grid(row=2, column=1, padx=5, pady=5)

    ctk.CTkLabel(insert_window, text="Gender:").grid(row=3, column=0, padx=5, pady=5)
    ctk.CTkEntry(insert_window, textvariable=gender_var).grid(row=3, column=1, padx=5, pady=5)

    ctk.CTkLabel(insert_window, text="Email:").grid(row=4, column=0, padx=5, pady=5)
    ctk.CTkEntry(insert_window, textvariable=email_var).grid(row=4, column=1, padx=5, pady=5)

    ctk.CTkLabel(insert_window, text="Mobile:").grid(row=5, column=0, padx=5, pady=5)
    ctk.CTkEntry(insert_window, textvariable=mobile_var).grid(row=5, column=1, padx=5, pady=5)

    ctk.CTkLabel(insert_window, text="Address:").grid(row=6, column=0, padx=5, pady=5)
    ctk.CTkEntry(insert_window, textvariable=address_var).grid(row=6, column=1, padx=5, pady=5)

    ctk.CTkButton(insert_window, text="Insert", command=insert_employee).grid(row=7, columnspan=2, pady=10)

def open_update_window():
    emp_id = simpledialog.askinteger("Input", "Enter Employee ID to Update:")
    if emp_id is None:
        return  # Cancelled

    # Fetch existing details
    query = "SELECT emp_name, role, age, gender, email, mobile, address FROM employees WHERE emp_id=%s"
    result = execute_query(query, (emp_id,))
    if not result:
        messagebox.showerror("Error", "Employee ID not found!")
        return

    existing_data = result[0]

    def update_employee():
        query = """
        UPDATE employees
        SET emp_name=%s, role=%s, age=%s, gender=%s, email=%s, mobile=%s, address=%s
        WHERE emp_id=%s
        """
        params = (emp_name_var.get(), role_var.get(), age_var.get(), gender_var.get(),
                  email_var.get(), mobile_var.get(), address_var.get(), emp_id)
        execute_query(query, params)
        load_employees()
        update_window.destroy()

    update_window = ctk.CTkToplevel()
    update_window.title("Update Employee")

    emp_name_var = ctk.StringVar(value=existing_data[0])
    role_var = ctk.StringVar(value=existing_data[1])
    age_var = ctk.IntVar(value=existing_data[2])
    gender_var = ctk.StringVar(value=existing_data[3])
    email_var = ctk.StringVar(value=existing_data[4])
    mobile_var = ctk.StringVar(value=existing_data[5])
    address_var = ctk.StringVar(value=existing_data[6])

    # Using grid to place fields in 2 columns
    ctk.CTkLabel(update_window, text="Employee Name").grid(row=0, column=0, padx=5, pady=5)
    ctk.CTkEntry(update_window, textvariable=emp_name_var).grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(update_window, text="Role").grid(row=1, column=0, padx=5, pady=5)
    ctk.CTkEntry(update_window, textvariable=role_var).grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(update_window, text="Age").grid(row=2, column=0, padx=5, pady=5)
    ctk.CTkEntry(update_window, textvariable=age_var).grid(row=2, column=1, padx=5, pady=5)

    ctk.CTkLabel(update_window, text="Gender").grid(row=3, column=0, padx=5, pady=5)
    ctk.CTkEntry(update_window, textvariable=gender_var).grid(row=3, column=1, padx=5, pady=5)

    ctk.CTkLabel(update_window, text="Email").grid(row=4, column=0, padx=5, pady=5)
    ctk.CTkEntry(update_window, textvariable=email_var).grid(row=4, column=1, padx=5, pady=5)

    ctk.CTkLabel(update_window, text="Mobile").grid(row=5, column=0, padx=5, pady=5)
    ctk.CTkEntry(update_window, textvariable=mobile_var).grid(row=5, column=1, padx=5, pady=5)

    ctk.CTkLabel(update_window, text="Address").grid(row=6, column=0, padx=5, pady=5)
    ctk.CTkEntry(update_window, textvariable=address_var).grid(row=6, column=1, padx=5, pady=5)

    ctk.CTkButton(update_window, text="Update", command=update_employee).grid(row=7, columnspan=2, pady=10)

def open_delete_window():
    emp_id = simpledialog.askinteger("Input", "Enter Employee ID to Delete:")
    if emp_id is None:
        return  # Cancelled

    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete employee ID {emp_id}?"):
        query = "DELETE FROM employee_credentials WHERE emp_id=%s"
        execute_query(query, (emp_id,))
        query = "DELETE FROM employees WHERE emp_id=%s"
        execute_query(query, (emp_id,))
        load_employees()

def open_admin_dashboard():
    dashboard_window = ctk.CTk()  
    dashboard_window.title("Admin Dashboard")
    
    # Frame for content
    frame = ctk.CTkFrame(dashboard_window)
    frame.pack(side="top", fill="both", expand=True)

    # Sidebar
    sidebar = ctk.CTkFrame(frame)
    sidebar.pack(side="left", fill="y")

    ctk.CTkButton(sidebar, text="Insert Employee", command=open_insert_window).pack(padx=10, pady=10)
    ctk.CTkButton(sidebar, text="Update Employee", command=open_update_window).pack(padx=10, pady=10)
    ctk.CTkButton(sidebar, text="Delete Employee", command=open_delete_window).pack(padx=10, pady=10)

    # Treeview for employee list
    global employee_tree
    employee_tree = ttk.Treeview(frame, columns=("emp_id", "emp_name", "role", "age", "gender", "email", "mobile", "address"), show="headings")
    employee_tree.pack(side="right", fill="both", expand=True)

    for col in employee_tree["columns"]:
        employee_tree.heading(col, text=col)

    load_employees()

    dashboard_window.mainloop()

# Start the application
#open_admin_dashboard()
