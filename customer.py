import customtkinter as ctk
from tkinter import messagebox, ttk
from tkinter import *
import tkinter as tk
import sv_ttk
from db_cn import execute_query

def tree_viewdt():
    for row in cmp_tree.get_children():
        cmp_tree.delete(row)
    r = execute_query("SELECT * from customers")
    for row in r:
        cmp_tree.insert('',END,values=row)

def cus_form(root):
    global cmp_tree
    cmp_frame = Frame(root, width=1070, height=567)
    cmp_frame.place(x=225, y=100)
    head_lbl = Label(cmp_frame, text="Customer Details", font=(None, 16), fg='white')
    head_lbl.place(x=0, y=0, relwidth=1)
    back_btn = ttk.Button(cmp_frame, text="Back", style='Accent.TButton', cursor='hand2', command=lambda: cmp_frame.place_forget())
    back_btn.place(x=0, y=30)

    topframe = Frame(cmp_frame)
    topframe.place(x=0, y=60, relwidth=1, height=500)

    search_frame = Frame(topframe)
    search_frame.pack()

    sea_box = ttk.Combobox(search_frame, values=("c_id", "c_name", "pass_mem"), state='readonly', font=(None, 12))
    sea_box.set('Search By')
    sea_box.grid(row=0, column=0, padx=10)


    search_entry = ttk.Entry(search_frame, font=(None, 12))
    search_entry.grid(row=0, column=1, padx=(0, 10))

    search_button = ttk.Button(search_frame, text="Search", style='Accent.TButton', cursor='hand2', width=10,command= lambda: search_cmp(sea_box.get(),search_entry.get()))
    search_button.grid(row=0, column=2, padx=(0, 10))
    show_button = ttk.Button(search_frame, text="Show All", style='Accent.TButton', cursor='hand2', width=10,command = lambda: show_all(sea_box,search_entry))
    show_button.grid(row=0, column=3)



    hori = Scrollbar(topframe, orient=HORIZONTAL,bg='grey')
    veri = Scrollbar(topframe, orient=VERTICAL,bg='grey',background='grey')

    cmp_tree = ttk.Treeview(topframe, columns=('c_id', 'c_name', 'age', 'mobile', 'total_spent', 'last_visit', 'pass_mem'),
                            show='headings', yscrollcommand=veri.set, xscrollcommand=hori.set,height=20)

    hori.pack(side=BOTTOM, fill=X)
    veri.pack(side=LEFT, fill=Y, pady=(10, 0))

    hori.config(command=cmp_tree.xview)
    veri.config(command=cmp_tree.yview)

    cmp_tree.heading('c_id', text='Customer ID')
    cmp_tree.heading('c_name', text='Customer Name')
    cmp_tree.heading('age', text='Age')
    cmp_tree.heading('mobile', text='Mobile')
    cmp_tree.heading('total_spent', text='Total Spent')
    cmp_tree.heading('last_visit', text='Last Visit')
    cmp_tree.heading('pass_mem', text='Password Member')

    cmp_tree.pack(fill=BOTH, padx=5, pady=(10, 10))
    tree_viewdt()

def show_all(opt,val):
    val.delete(0,END)
    opt.set("Search By")
    
    tree_viewdt()

def search_cmp(opt,val):
    print("HI")
    if opt=="Search By":
        messagebox.showerror("Error","No option is selected")
    elif val=="":
        messagebox.showerror("Error","No value is entered")
    else:
        r=execute_query(f"SELECT * from customers where {opt} like %s",(f'%{val}%',))
        cmp_tree.delete(*cmp_tree.get_children())
        for row in r:
            cmp_tree.insert('',END,value=row)