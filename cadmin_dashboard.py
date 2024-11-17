import customtkinter as ctk
from tkinter import messagebox, ttk, Label, Frame
from db_cn import execute_query
from em import employee_form
from customer import cus_form
from chg_pass import change_pass
from stock_details import stock_form

from datetime import datetime
import sv_ttk
import tkinter as tk
from stas_report import sta_rep

def quit_fun(root):
    if messagebox.askyesno('Confirmation', "Are you sure?"):
        root.destroy()

def log_out_fn(root):
    if messagebox.askyesno('Confirmation', 'Do you want to log out?'):
        from clogin import run_login_page
        root.destroy()
        run_login_page()

def update_time(label):
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().date()
    label.config(text=f"\t\t\t\t\t\t\t\t\t\t\t{current_date}   {current_time}")  # Update the label with date and time
    label.after(1000, update_time, label)  # Schedule the next update after 1 second

def open_admin_dashboard(user_id):
    root = tk.Tk()
    root.title("Admin Dashboard")
    style = ttk.Style(root)
    root.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-dark")

    root.geometry('1278x668+0+0')
    root.resizable(0, 0)

    # Title Label
    tit_lab = Label(root, text="Hyper-Market Management", font=(None, 25, 'bold'), bg="#111111", fg='white')
    tit_lab.place(x=0, y=0, relwidth=1)

    # Logout Button
    lg_btn = ttk.Button(root, text="Logout", style='Accent.TButton', width=10, command=lambda: log_out_fn(root), cursor='hand2')
    lg_btn.place(x=1150, y=5)

    # Subtitle Label with date and time
    sub_tlt = Label(root, font=('Arial', 14))
    sub_tlt.place(x=0, y=50, relwidth=1)
    update_time(sub_tlt)  # Start updating the time on the same label

    # Frame for Widgets
    wid_frm = Frame(root)
    wid_frm.pack(anchor='w', padx=5, pady=(50, 0))  # Add padding to push it down

    # Left Menu LabelFrame
    left_menu = ttk.LabelFrame(wid_frm, text="Menu")
    left_menu.grid(row=0, column=0, padx=5, pady=20)

    # Menu Labels
    menuLabel = Label(left_menu, text="MENU", font=(None, 25, 'bold'))
    menuLabel.grid(row=0, column=0, sticky='nsew', pady=(0, 20))  # Add some vertical space below

    # Buttons in the Left Menu
    emp_button = ttk.Button(left_menu, text="Employee",cursor='hand2', padding=(10, 10), width=20, command=lambda: employee_form(root))
    emp_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

    cus_button = ttk.Button(left_menu, text="Customer", padding=(10, 10), cursor='hand2',width=20, command=lambda: cus_form(root))
    cus_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

    sales_button = ttk.Button(left_menu, text="Stock Details", padding=(10, 10), width=20,cursor='hand2',command= lambda : stock_form(root))
    sales_button.grid(row=3, column=0, padx=10, pady=10, sticky='ew')

    report_button = ttk.Button(left_menu, text="Statistical Reports", padding=(10, 10), width=20,cursor='hand2', command = lambda: sta_rep(root))
    report_button.grid(row=4, column=0, padx=10, pady=10, sticky='ew')

    delivery_button = ttk.Button(left_menu, text="Change Password", padding=(10, 10), width=20,cursor='hand2', command=lambda: change_pass(root, user_id))
    delivery_button.grid(row=5, column=0, padx=10, pady=10, sticky='ew')

    quit_button = ttk.Button(left_menu, text="Quit", padding=(10, 10), width=20,cursor='hand2', command=lambda: quit_fun(root))
    quit_button.grid(row=6, column=0, padx=10, pady=10, sticky='ew')

    employee_form(root)

    # Status Frames
    status_frame_configurations = [
        ("Net Revenue:", "0", 250, 175),
        ("Total Profit:", "0", 800, 175),
        ("Total Checkouts:", "0", 250, 350),
        ("Pending Deliveries:", "0", 800, 350),
        ("Bill Amount Due:", "0", 500, 500),
    ]
    
    sv_ttk.set_theme("dark")
    root.mainloop()
