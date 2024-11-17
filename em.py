import customtkinter as ctk
from tkinter import messagebox, simpledialog, ttk
from db_cn import execute_query
from tkinter import *
import tkinter as tk
import sv_ttk

def tree_viewdt():
    for row in emp_tree.get_children():
        emp_tree.delete(row)
    r = execute_query("SELECT * from employees")
    for row in r:
        emp_tree.insert('',END,values=row)

def add_emp(id,name,role,gender,age,email,mobile,ad,id_box):
    id_box.config(state=NORMAL)
    gender = "M" if gender == "Male" else "F"
    d = [id,name,role,age,gender,email,mobile,ad]
    if any(x=='' for x in d):
        messagebox.showerror("Error","All fields are required")
    else:
       
        query = "SELECT emp_id from employees where emp_id=%s"
        r = execute_query(query,(id,))
        if r:
            messagebox.showerror("Error","Employee ID already exists")
        else:
            query = "INSERT into employees values(%s,%s,%s,%s,%s,%s,%s,%s)"
            execute_query(query,d)
            query = "INSERT into employee_credentials values(%s,%s,%s)"
            execute_query(query,(id,role,"Changeme@123"))
            emp_tree.delete(emp_tree.get_children())
            tree_viewdt()
            messagebox.showinfo("Success","Data is inserted successfully")

def select_data(id,name,role,gender,age,email,mobile,ad):

    clr(id,name,role,gender,age,email,mobile,ad,0)
    index = emp_tree.selection()
    val = emp_tree.item(index)
    d = [id,name,role,age,gender,email,mobile,ad]   

    r = val['values']
    for i,v in enumerate(r):
        d[i].insert(0,v)
    id.config(state=DISABLED)

def upd_emp(id,name,role,age,gender,email,mobile,address):
    sel = emp_tree.selection()
    if not sel:
        messagebox.showerror("Error","Select a field")
    else:
        r = execute_query("SELECT * FROM employees where emp_id=%s",(id,))
        r=r[0]
        d = [id,name,role,age,gender,email,mobile,address]
        
        gender = "M" if gender=="Male" else "F"
        if all(str(d[i]) == str(r[i]) for i in range(len(d))):
            messagebox.showwarning("No changes","No changes detected")
        else:
        
            query = update_query = """UPDATE employees
        SET emp_name=%s, role=%s, age=%s, gender=%s, email=%s, mobile=%s, address=%s
        WHERE emp_id=%s"""
            d = [name,role,age,gender,email,mobile,address,id]
            execute_query(query,d)
            execute_query("UPDATE employee_credentials set role=%s WHERE emp_id=%s",(role,id))
            messagebox.showinfo('Success',"Data updated successfully")
            tree_viewdt()

def delete_emp(id):
    sel = emp_tree.selection()
    if not sel:
        messagebox.showerror("Error","Select a field")
    else:
        r = messagebox.askyesno("Confirm","This can't be undone")
        if r:
            execute_query('Delete from employee_credentials where emp_id=%s',(id,))
            execute_query('Delete from employees where emp_id=%s',(id,))
            messagebox.showinfo("","Record deleted")
            tree_viewdt()

def clr(id,name,role,gender,age,email,mobile,ad,c):
    d = [id,name,role,age,gender,email,mobile,ad]  
    id.config(state=NORMAL) 
    [x.delete(0,END)for x in d]
    if c:
        emp_tree.selection_remove(emp_tree.selection())
    
def employee_form(root):
    global emp_tree
    emp_frame = Frame(root, width=1070, height=567)
    emp_frame.place(x=225, y=100)
    head_lbl = Label(emp_frame, text="Manage Employee Details", font=(None, 18,'bold'), fg='white')
    head_lbl.place(x=0, y=0, relwidth=1)
    #back_btn = ttk.Button(emp_frame, text="Back",style='Accent.TButton', cursor='hand2', command=lambda: emp_frame.place_forget())
    #back_btn.place(x=0, y=30)

    topframe = Frame(emp_frame)
    topframe.place(x=0, y=60, relwidth=1, height=235)

    search_frame = Frame(topframe)
    search_frame.pack()
    sea_box = ttk.Combobox(search_frame, values=("emp_id", "emp_name", "role"), state='readonly', font=(None, 12))
    sea_box.set('Search By')
    sea_box.grid(row=0, column=0, padx=20)

    search_entry = ttk.Entry(search_frame, font=(None, 14))
    search_entry.grid(row=0, column=1)
    search_button = ttk.Button(search_frame, text="Search",style='Accent.TButton', cursor='hand2', width=10,command= lambda: search_emp(sea_box.get(),search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)
    show_button = ttk.Button(search_frame, text="Show All",style='Accent.TButton', cursor='hand2', width=10,command = lambda: show_all(sea_box,search_entry))
    show_button.grid(row=0, column=3)

    # Horizontal and Vertical Scrollbars
    hori = Scrollbar(topframe, orient=HORIZONTAL)
    veri = Scrollbar(topframe, orient=VERTICAL)

    emp_tree = ttk.Treeview(topframe, columns=('emp_id', 'emp_name', 'role', 'age', 'gender', 'email', 'mobile', 'address'),
                            show='headings', yscrollcommand=veri.set, xscrollcommand=hori.set)

    # Configure Scrollbars
    hori.pack(side=BOTTOM, fill=X)
    veri.pack(side=RIGHT, fill=Y,pady=(10,0))

    hori.config(command=emp_tree.xview)
    veri.config(command=emp_tree.yview)

    # Define Treeview Headings
    emp_tree.heading('emp_id', text='Employee ID')
    emp_tree.heading('emp_name', text='Employee Name')
    emp_tree.heading('role', text='Role')
    emp_tree.heading('age', text='Age')
    emp_tree.heading('gender', text='Gender')
    emp_tree.heading('email', text='Email')
    emp_tree.heading('mobile', text='Mobile')
    emp_tree.heading('address', text='Address')

    # Define Column Widths

    emp_tree.pack(fill=BOTH, pady=(10, 0))

    details_frame = Frame(emp_frame)
    details_frame.place(x=0,y=300)
    
    empid_label = Label(details_frame,text="Employee Id:",font=('Arial',12))
    empid_label.grid(row=0,column=0,padx=(20,10),pady=10)
    empid_entry=ttk.Entry(details_frame,font=(None,12))
    empid_entry.grid(row=0,column=1,padx=(5,20),pady=10)
    
    name_label = Label(details_frame,text="Name:",font=('Arial',12))
    name_label.grid(row=0,column=2,padx=20,pady=10)
    name_entry=ttk.Entry(details_frame,font=(None,12))
    name_entry.grid(row=0,column=3,padx=(5,20),pady=10)
    
    role_label = Label(details_frame,text="Role:",font=('Arial',12))
    role_label.grid(row=0,column=4,padx=20,pady=10)
    role_entry=ttk.Combobox(details_frame,font=(None,10),values=('Admin','Cashier','Stock Manager'))
    role_entry.grid(row=0,column=5,padx=(5,20),pady=10)
    
    d_label = Label(details_frame,text="Gender:",font=('Arial',12))
    d_label.grid(row=1,column=0,padx=20,pady=10)
    d_entry=ttk.Combobox(details_frame,values=("Male","Female"),font=(None,10))
    d_entry.grid(row=1,column=1,padx=(5,20),pady=10)

    a_label = Label(details_frame,text="Age:",font=('Arial',12))
    a_label.grid(row=1,column=2,padx=20,pady=10)
    a_entry=ttk.Entry(details_frame,font=(None,12))
    a_entry.grid(row=1,column=3,padx=(5,20),pady=10)

    e_label = Label(details_frame,text="Email:",font=('Arial',12))
    e_label.grid(row=1,column=4,padx=20,pady=10)
    e_entry=ttk.Entry(details_frame,font=(None,12))
    e_entry.grid(row=1,column=5,padx=(5,20),pady=10)

    m_label = Label(details_frame,text="Mobile:",font=('Arial',12))
    m_label.grid(row=2,column=0,padx=20,pady=10)
    m_entry=ttk.Entry(details_frame,font=(None,12))
    m_entry.grid(row=2,column=1,padx=(5,20),pady=10)
    
    Ad_label = Label(details_frame,text="Address:",font=('Arial',12))
    Ad_label.grid(row=2,column=2,padx=20,pady=10)
    Ad_entry=ttk.Entry(details_frame,font=(None,12))
    Ad_entry.grid(row=2,column=3,padx=(5,20),pady=10)

    btn_frm = Frame(emp_frame)
    btn_frm.place(x=200,y=490)
    add_button = ttk.Button(btn_frm, text="Add", cursor='hand2',style='Accent.TButton', width=10,command = lambda : add_emp(empid_entry.get(),name_entry.get(),role_entry.get()
                            ,d_entry.get(),a_entry.get(),e_entry.get(),m_entry.get(),Ad_entry.get(),empid_entry))
    add_button.grid(row=0, column=0, padx=20)
    update_button = ttk.Button(btn_frm, text="Update", cursor='hand2',style='Accent.TButton', width=10,command= lambda : upd_emp(empid_entry.get(),name_entry.get(),role_entry.get()
                            ,a_entry.get(),d_entry.get(),e_entry.get(),m_entry.get(),Ad_entry.get()))
    update_button.grid(row=0, column=1,padx=20)
    Delete_button = ttk.Button(btn_frm, text="Delete", cursor='hand2',style='Accent.TButton', width=10,command=lambda :delete_emp(empid_entry.get()))
    Delete_button.grid(row=0, column=2,padx=20)
    Clear_button = ttk.Button(btn_frm, text="Clear", cursor='hand2',style='Accent.TButton', width=10,command= lambda :clr(empid_entry,name_entry,role_entry
                            ,d_entry,a_entry,e_entry,m_entry,Ad_entry,1))
    Clear_button.grid(row=0, column=3,padx=20)
    emp_tree.bind('<ButtonRelease-1>',lambda event: select_data(empid_entry,name_entry,role_entry
                            ,d_entry,a_entry,e_entry,m_entry,Ad_entry))
    
    
    
    tree_viewdt()
def search_emp(opt,val):
    
    if opt=="Search By":
        messagebox.showerror("Error","No option is selected")
    elif val=="":
        messagebox.showerror("Error","No value is entered")
    else:
        r=execute_query(f"SELECT * from employees where {opt} like %s",(f'%{val}%',))
        emp_tree.delete(*emp_tree.get_children())
        for row in r:
            emp_tree.insert('',END,value=row)

def show_all(opt,val):
    val.delete(0,END)
    opt.set("Search By")
    tree_viewdt()
