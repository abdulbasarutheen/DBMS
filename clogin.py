import customtkinter as ctk
from tkinter import messagebox
from db_cn import execute_query
from cadmin_dashboard import open_admin_dashboard 
from cashier_dashboard import cashier_dashboard
from StockManagerDB import open_stock

role_list = ["Admin", "Cashier", "Stock Manager"]

def run_login_page():
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue")  

    root = ctk.CTk()  
    root.title("Login page")

    def toggle_password():
        if Mode_swtch.get():  
            pass_entry.configure(show="")  # Show password
        else:
            pass_entry.configure(show="*")  # Hide password

    def log_click():
        name = name_entry.get()
        password = pass_entry.get()
        role = role_cb.get()
        details = [name, password, role]

        if any(x == "" for x in details):
            messagebox.showerror("Error", "All fields are required!")
            return

        result = execute_query(f"SELECT password, role from employee_credentials where emp_id={name}")
        if result:
            pas, r = result[0]
            if (password == pas and r == role):
                
                messagebox.showinfo("Yahoo", "Login successful!")
                root.destroy()
                if role=='Admin': 
                    open_admin_dashboard(name)
                elif role=='Cashier':
                    cashier_dashboard(name)
                elif role=="Stock Manager":
                    open_stock(name)
            else:
                messagebox.showerror("Wrong credentials", "Incorrect credentials are entered")
        else:
            messagebox.showerror("Wrong Info", "No employee is found with that ID")

    frame = ctk.CTkFrame(root)
    frame.pack(pady=20, padx=20)

    name_label = ctk.CTkLabel(frame, text="Log In", font=('Arial', 20, 'bold'))
    name_label.pack(pady=(10, 0))

    widgets_frame = ctk.CTkFrame(frame)
    widgets_frame.pack(padx=20, pady=10)

    name_label = ctk.CTkLabel(widgets_frame, text="Employee Id:")
    name_label.grid(row=0, column=0, padx=5, pady=(5, 5), sticky='w')
    name_entry = ctk.CTkEntry(widgets_frame)
    name_entry.grid(row=1, column=0, padx=5, pady=(0, 5), sticky='ew')

    pass_label = ctk.CTkLabel(widgets_frame, text="Password:")
    pass_label.grid(row=2, column=0, padx=5, pady=(5, 5), sticky='w')
    pass_entry = ctk.CTkEntry(widgets_frame, show='*')
    pass_entry.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

    role_label = ctk.CTkLabel(widgets_frame, text="Select role:")
    role_label.grid(row=5, column=0, padx=5, pady=(5, 5), sticky='w')
    role_cb = ctk.CTkComboBox(widgets_frame, values=role_list, state='readonly')
    role_cb.set(role_list[0])  
    role_cb.grid(row=6, column=0, padx=5, pady=5, sticky='ew')

    lg_btn = ctk.CTkButton(widgets_frame, text="Login", command=log_click)
    lg_btn.grid(row=8, column=0, padx=5, pady=10, sticky='nsew')

    separator = ctk.CTkFrame(widgets_frame, height=2, width=400, corner_radius=0)
    separator.grid(row=7, column=0, padx=(20, 10), pady=10, sticky="ew")

    Mode_swtch = ctk.CTkSwitch(widgets_frame, text="Show Password", command=toggle_password)
    Mode_swtch.grid(row=4, column=0, padx=20, pady=10, sticky="e")

    root.mainloop()

if __name__ == '__main__':
    run_login_page()
