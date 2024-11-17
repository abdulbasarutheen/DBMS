import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db_cn import execute_query
from admin_dashboard import open_admin_dashboard 


role_list = ["Admin","Cashier","Stock Manager"]


root = tk.Tk()
root.title("Login page")
style = ttk.Style(root)
root.tk.call("source","forest-dark.tcl")
root.tk.call("source","forest-light.tcl")
style.theme_use("forest-dark")

def toggle_mode():
    if Mode_swtch.instate(["selected"]):
        style.theme_use("forest-light")
    else:
        style.theme_use("forest-dark")
    
def log_click():
    name = name_entry.get()
    password = pass_entry.get()
    role = role_cb.get()
    details = [name,password,role]
    f=1
    if any(x=="" for x in details):
        messagebox.showerror("Error","All fields are required!")
        return
    result = execute_query(f"SELECT password, role from employee_credentials where emp_id={name}")
    if result:

        pas,r  = result[0]
        if (password==pas and r==role):
            messagebox.showinfo("Yahoo","Login successfull!")
            root.destroy()
            open_admin_dashboard()
        else:
            messagebox.showerror("Wrong credentials","Incorrect credentials are entered")
    else:
        messagebox.showerror("Wrong Info","No employee is found with that ID")

        
frame = ttk.Frame(root)
frame.pack()

widgets_frame = ttk.LabelFrame(frame)
widgets_frame.grid(row=0,column=0,padx=20,pady=10)

name_label = ttk.Label(widgets_frame,text="Employee Id:")
name_label.grid(row=0,column=0,padx=5,pady=(5,5),sticky='ew')
name_entry = ttk.Entry(widgets_frame)

name_entry.grid(row=1,column=0, padx=5, pady=(0,5), sticky='ew')

pass_label = ttk.Label(widgets_frame,text="Password:")
pass_label.grid(row=2,column=0,padx=5,pady=(5,5),sticky='ew')
pass_entry = ttk.Entry(widgets_frame,show='*')

pass_entry.grid(row=3,column=0, padx=5, pady=5, sticky='ew')

role_label = ttk.Label(widgets_frame,text="Select role:")
role_label.grid(row=4,column=0,padx=5,pady=(5,5),sticky='ew')
role_cb = ttk.Combobox(widgets_frame,values=role_list)
role_cb.current(0)
role_cb.grid(row=5,column=0,padx=5, pady=5, sticky='ew')

lg_btn = ttk.Button(widgets_frame,text="Login",command=log_click)
lg_btn.grid(row=6,column=0,padx=5, pady=10,sticky='nsew')

seperator = ttk.Separator(widgets_frame)
seperator.grid(row=7,column=0,padx=(20,10),pady=10, sticky = "ew")

Mode_swtch = ttk.Checkbutton(widgets_frame,text="Mode",style='Switch', command=toggle_mode)
Mode_swtch.grid(row=8,column=0,padx=5,pady=10,sticky="nsew")

root.mainloop()