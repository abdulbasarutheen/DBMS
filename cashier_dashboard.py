import customtkinter as ctk
from tkinter import messagebox, simpledialog, ttk
from db_cn import execute_query
from em import employee_form
from customer import cus_form
from chg_pass import change_pass
from tkinter import Menu
from invoice import invoice_gen


from tkinter import *
import tkinter as tk
import sv_ttk


from datetime import datetime


import tkinter as tk
from datetime import datetime


def update_time(label):
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().date()
    label.config(text=f"Welcome cashier\t\t Date: {current_date}\t\t Time: {current_time}")
   
    label.after(1000, update_time, label)



current_datetime = datetime.now()
current_date = datetime.now().date() 
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
name=""
total = 0.0
quan = 0

def delete_all_items(val):

    global total
    all_items = c_tree.get_children() 

    for item in all_items:
        row_values = c_tree.item(item, 'values')
        print("Processing item with product_id:", row_values[0])
        v = execute_query("SELECT quantity from inventory where product_id=%s",(row_values[0],))[0][0]
        if v < 10:
            select_query = "SELECT last_reported FROM notify WHERE product_id = %s"
            result = execute_query(select_query, (row_values[0],))
            
            if result:
                update_query = """
                    UPDATE notify 
                    SET last_reported = %s, 
                        no_of_out_of_stock = no_of_out_of_stock + 1, 
                        current_stock = %s 
                    WHERE product_id = %s
                """
                execute_query(update_query, (formatted_datetime, v, row_values[0]))
            else: 
                insert_query = """
                    INSERT INTO notify (product_id, reported_by, last_reported, no_of_out_of_stock, current_stock) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                execute_query(insert_query, (row_values[0], user_id, formatted_datetime, 1, v))  # no_of_out_of_stock starts from 1

        
        if val: 
            print("Updating inventory for product_id:", row_values[0])
            
            execute_query(
                "UPDATE inventory SET quantity = quantity + %s WHERE product_id = %s", 
                (row_values[2], row_values[0])
            )
        
        
        c_tree.delete(item)
    total=0

def tree_viewdt():
    for row in p_tree.get_children():
        p_tree.delete(row)
    r = execute_query("SELECT product_id,product_name,category,price from inventory")
    for row in r:
        p_tree.insert('',END,values=row)

def ctree_viewdt(id,name,quantity,tot):
    global total
    global quan
    total += float(tot)
    quan += int(quantity)
    execute_query(f"UPDATE inventory SET quantity = quantity - %s WHERE product_id = %s", (quantity, id))
    r = (id,name,quantity,tot)
    
    c_tree.insert('',END,values=r)

def log_out_fn(root):
    f = messagebox.askyesno('Confirmation', 'Do you want to log out?')
    if f:
        from clogin import run_login_page
        root.destroy()
        run_login_page()

def clr():
    name_entry.config(state=NORMAL)
    d = [id_entry,name_entry,qtn_entry]   
    [x.delete(0,END)for x in d]

def select_data():
    clr()
    index = p_tree.selection()
    val = p_tree.item(index)
    r = val['values']
    print(r)
    d = [id_entry,name_entry]   
    for i in range(2):
        d[i].insert(0,r[i])
    name_entry.config(state=DISABLED)
def get_cid():
    f = execute_query("Select c_id from customers where mobile=%s",(mobile_number,))
    print(f[0][0])
    return f[0][0]
def upd_sales(t_mode):
    f = get_cid()
    execute_query("INSERT into sales (emp_id,customer_id,quantity,total_amount,sale_date,payment_method) values (%s,%s,%s,%s,%s,%s)",(user_id,f,quan,total,formatted_datetime,t_mode))
def checkout():
    global mobile_number
    mobile_number = m_entry.get()
    global t_mode
    t_mode = pm_cb.get()
    m_entry.delete(0,END)
    pm_cb.set("Select Payment mode")
    
   
    existing_customer = execute_query("SELECT * FROM customers WHERE mobile=%s", (mobile_number,))
    if existing_customer:
        execute_query("UPDATE customers SET last_visit = CURDATE(), total_spent = total_spent + %s WHERE mobile = %s", 
                  (total, mobile_number))
        upd_sales(t_mode)
        retrieve_ctree_data()
    else:
        ask_for_customer_details(mobile_number)
    
    

def ask_for_customer_details(mobile_number):
  
    details_window = tk.Toplevel(root)
    details_window.title("Customer Details")

    frame = Frame(details_window)
    frame.pack(pady=20, padx=20)

    c_label = Label(frame, text="Customer Details", font=('Arial', 20, 'bold'))
    c_label.pack(pady=(10, 0))
    widgets_frame = Frame(frame)
    widgets_frame.pack(padx=20, pady=10)

    c_label = ttk.Label(widgets_frame, text="Name:")
    c_label.grid(row=0, column=0, padx=5, pady=(5, 5), sticky='w')
    c_name = ttk.Entry(widgets_frame)
    c_name.grid(row=1, column=0, padx=5, pady=(5, 5), sticky='w')

    a_label = ttk.Label(widgets_frame, text="Age:")
    a_label.grid(row=2, column=0, padx=5, pady=(5, 5), sticky='w')
    c_age = ttk.Entry(widgets_frame)
    c_age.grid(row=3, column=0, padx=5, pady=(5, 5), sticky='w')

    p_label = ttk.Label(widgets_frame, text="Avail Membership:")
    p_label.grid(row=4, column=0, padx=5, pady=(5, 5), sticky='w')
   
    switch_var = tk.IntVar()  
    c_pass_yes = ttk.Radiobutton(widgets_frame, text="Yes", variable=switch_var, value=1)
    c_pass_yes.grid(row=5, column=0, padx=5, pady=(5, 5), sticky='w')
    c_pass_no = ttk.Radiobutton(widgets_frame, text="No", variable=switch_var, value=0)
    c_pass_no.grid(row=5, column=1, padx=5, pady=(5, 5), sticky='w')

    sub = ttk.Button(widgets_frame, text="Submit", cursor='hand2', command=lambda: submit_details(c_name, c_age, switch_var.get(), mobile_number,details_window))
    sub.grid(row=6, column=0, padx=5, pady=5, sticky='ew')

def submit_details(name_entry, age_entry, pass_member_value, mobile_number,details_window):
    global name
    name = name_entry.get()
    age = age_entry.get()

    if not name or not age or not mobile_number:
        messagebox.showerror("Error", "All fields are required")
        return

    execute_query("INSERT INTO customers (c_name, age, mobile, total_spent, last_visit, pass_mem) VALUES (%s, %s, %s, %s, %s, %s)", 
                      (name, age, mobile_number, total, current_date, pass_member_value))
    messagebox.showinfo("Success", "Customer details saved. Proceeding to checkout.")
    upd_sales(t_mode)
    retrieve_ctree_data()
    details_window.destroy()


def add_fn():
    id = id_entry.get().strip()
    qtn = qtn_entry.get().strip()
    if id=="" or qtn =="":
        messagebox.showerror("Error","All fields are required")
    else:
        f=execute_query("SELECT quantity,price,product_name from inventory where product_id=%s",(id,))
        if f:
            y=1
            if f[0][0] < int(qtn) and f[0][0]>0:
                y= messagebox.askyesno("Warning",f"Only {f[0][0]} stocks left, Add available stocks? ")
                qtn = f[0][0]
            elif f[0][0]==0:
                b =messagebox.askokcancel("Warning","Out of stock, Stock Manager is Notified!")
                y=0
            if y:
                ctree_viewdt(id,f[0][2],qtn,f[0][1]*int(qtn))
        else:
            messagebox.showerror('Error',"Product Id doesn't exist")

def check_fn():
    mobile = m_entry.get().strip()
    p_type = pm_cb.get()
    if mobile=="" or p_type=="Select Payment mode":
        messagebox.showerror("Error","Fill all fields properly")
    else:
        checkout()
def upd_c():
    sel = c_tree.selection()
    if not sel:
        messagebox.showerror("Error","Select a field")
    
    else:
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected row?")
        if confirm:
            
            for item in sel:
                global total
                global quan
                row_values = c_tree.item(item, 'values')
                execute_query(f"UPDATE inventory SET quantity = quantity + %s WHERE product_id = %s", (row_values[2], row_values[0]))
                tot_value = float(row_values[3])
                total -= tot_value
                quan -= int(row_values[2])
                c_tree.delete(item)  

            messagebox.showinfo("Success", "Selected row has been removed.")

def cashier_dashboard(e_id): 
    global user_id
    user_id = int(e_id)
    global root
    root = tk.Tk()
    root.title("Cashier Dashboard")
    style = ttk.Style(root)
    root.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-dark")

    root.geometry('1278x668+0+0')
    root.resizable(0, 0)

    tit_lab = Label(root, text="BILLING SYSTEM", font=('inter', 25, 'bold'), bg="#111111", fg='white')
    tit_lab.place(x=0, y=0, relwidth=1)


    lg_btn = ttk.Button(root, text="Logout", style='Accent.TButton', width=10, command=lambda: log_out_fn(root))
    lg_btn.place(x=1170, y=5)


    dframe = Frame(root)  
    dframe.place(x=0, y=60, width=600, height=450)

    wid_frame = Frame(root)
    wid_frame.place(x=0,y=510,width=600,height=158)

    product_lb = Label(dframe, text="Product details", font=('inter', 20, 'bold'))
    product_lb.pack(padx=10, pady=10)

    sub_tlt = Label(root, font=('Arial', 16))
    sub_tlt.place(x=0, y=37, relwidth=1)
    update_time(sub_tlt)

    hori = Scrollbar(dframe, orient=HORIZONTAL)
    veri = Scrollbar(dframe, orient=VERTICAL)

    global p_tree
    p_tree = ttk.Treeview(dframe, columns=('product_id', 'product_name', 'category', 'price'),
                            show='headings', yscrollcommand=veri.set, xscrollcommand=hori.set, height=15)



    veri.pack(side=RIGHT, fill=Y, pady=(10, 0))
    veri.config(command=p_tree.yview)


    p_tree.heading('product_id', text='Product ID')
    p_tree.heading('product_name', text='Product Name')
    p_tree.heading('category', text='Category')
    p_tree.heading('price', text='Price')


    p_tree.column('product_id', width=100)
    p_tree.column('product_name', width=200)
    p_tree.column('category', width=150)
    p_tree.column('price', width=100)


    p_tree.pack(fill=BOTH, pady=(10, 0),padx=(20,0))
    p_tree.bind('<ButtonRelease-1>',lambda event: select_data())
    
    global id_entry,name_entry,qtn_entry

    id_label = Label(wid_frame,text="Product Id:",font=('Arial',10))
    id_label.grid(row=0,column=0,padx=(20,10),pady=(20,10))
    id_entry=ttk.Entry(wid_frame,font=(None,10))
    id_entry.grid(row=0,column=1,padx=(5,20),pady=10)
        
    name_label = Label(wid_frame,text="Product Name:",font=('Arial',10))
    name_label.grid(row=0,column=2,padx=20,pady=(20,10))
    name_entry=ttk.Entry(wid_frame,font=(None,10))
    name_entry.grid(row=0,column=3,padx=(5,20),pady=10)

    qtn_label = Label(wid_frame,text="Quantity :",font=('Arial',10))
    qtn_label.grid(row=1,column=0,padx=20,pady=10)
    qtn_entry=ttk.Entry(wid_frame,font=(None,10))
    qtn_entry.grid(row=1,column=1,padx=(5,20),pady=10)

    add_to_crt = ttk.Button(wid_frame,text="ADD TO CART",cursor='hand2',width=15,style='Accent.TButton',command= lambda: add_fn())
    add_to_crt.grid(row=1,column=3,padx=(5,20),pady=10)

    tree_viewdt()

    cframe = Frame(root)  
    cframe.place(x=600, y=60, width=600, height=450)

    product_lb = Label(cframe, text="Cart", font=('inter', 20, 'bold'))
    product_lb.pack(padx=10, pady=10)

    hori = Scrollbar(cframe, orient=HORIZONTAL)
    veri = Scrollbar(cframe, orient=VERTICAL)
    global c_tree
    c_tree = ttk.Treeview(cframe, columns=('product_id', 'product_name', 'quantity', 'total'),
                            show='headings', yscrollcommand=veri.set, xscrollcommand=hori.set, height=15)


    veri.pack(side=RIGHT, fill=Y, pady=(10, 0))
    veri.config(command=c_tree.yview)

    c_tree.heading('product_id', text='Product ID')
    c_tree.heading('product_name', text='Product Name')
    c_tree.heading('quantity', text='Quantity')
    c_tree.heading('total', text='Total')

    c_tree.column('product_id', width=100)
    c_tree.column('product_name', width=200)
    c_tree.column('quantity', width=100)
    c_tree.column('total', width=100)

    c_tree.pack(fill=BOTH, pady=(10, 0),padx=(50,0))

    wid_frame2 = Frame(root)
    wid_frame2.place(x=600,y=510,width=600,height=158)  

    global m_entry,pm_cb

    m_label = Label(wid_frame2,text="Customer Mobile:",font=('Arial',10))
    m_label.grid(row=0,column=0,padx=(60,0),pady=(20,10))
    m_entry=ttk.Entry(wid_frame2,font=(None,10),width=14)
    m_entry.grid(row=0,column=1,padx=10,pady=10)

    pm_cb = ttk.Combobox(wid_frame2,values=('online','cash','card'),font=('Arial',10),width=14)
    pm_cb.set("Select Payment mode")
    pm_cb.grid(row=0,column=2,padx=10,pady=10)


    rem_btn = ttk.Button(wid_frame2,text="REMOVE",cursor='hand2',width=15,style='Accent.TButton',command = lambda : upd_c())
    rem_btn.grid(row=1,column=0,padx=(50,10),pady=10)
    clr_btn = ttk.Button(wid_frame2,text="CLEAR",cursor='hand2',width=15,style='Accent.TButton',command = lambda : delete_all_items(1))
    clr_btn.grid(row=1,column=1,padx=10,pady=10)

    ckcrt = ttk.Button(wid_frame2,text="CHECK OUT",cursor='hand2',width=15,style='Accent.TButton',command= lambda : check_fn())
    ckcrt.grid(row=1,column=2,padx=10,pady=10)
    print(name)
    sv_ttk.set_theme("dark")
    root.mainloop()

def retrieve_ctree_data():
    
    nested_list = []

    tree_items = c_tree.get_children()
   
    for item in tree_items:
        
        values = c_tree.item(item, 'values')
        nested_list.append(values)  
    e_name = execute_query("select emp_name from employees where emp_id=%s",(user_id,))[0][0]
    bill_no = execute_query("SELECT sale_id FROM sales ORDER BY sale_id DESC LIMIT 1;")[0][0]
    ds = execute_query("SELECT pass_mem from customers where mobile=%s",(mobile_number,))[0][0]
    name = execute_query("SELECT c_name from customers where mobile=%s",(mobile_number,))[0][0]
    ds = 5 if ds==1 else 0
    invoice_gen(name,mobile_number,e_name,user_id,bill_no,formatted_datetime,nested_list,ds)
    print(name,mobile_number,e_name,user_id,bill_no,formatted_datetime,nested_list,ds)
    messagebox.showinfo("Info","Invoice generated successfully!")
    delete_all_items(0)
    