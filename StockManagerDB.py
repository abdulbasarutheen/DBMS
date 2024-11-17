import customtkinter as ctk
from tkinter import messagebox, ttk, Label, Frame
from db_cn import execute_query
from datetime import datetime
import tkinter as tk
import sv_ttk
from tkinter import *

def up_ntf():
    stock_value = stock.get().strip()
    price_value = price.get().strip()
    
    if not (stock_value.replace('.', '', 1).isdigit() and price_value.replace('.', '', 1).isdigit()):
        messagebox.showerror("Error", "Please enter valid numeric values for stock and price.")
        return  

    current_stock = float(stock_value)
    current_price = float(price_value)

    # Check if the values are updated
    if current_stock == s and current_price == p:
        messagebox.showerror("Error", "No values are updated")
        return

    # Get the selected product ID from n_tree or s_tree
    if n_tree.selection():
        product_id = n_tree.item(n_tree.selection())['values'][0]
        update_query = "UPDATE inventory SET quantity = %s, price = %s WHERE product_id = %s"
        params = (current_stock, current_price, product_id)
        execute_query(update_query, params) 
        messagebox.showinfo("Success", "Data updated successfully in the database")
        execute_query("DELETE FROM notify WHERE product_id = %s", (product_id,))
        tree_viewdt() 
        stree_viewdt() # Refresh the notification treeview
    elif s_tree.selection():
        product_id = s_tree.item(s_tree.selection())['values'][0]
        update_query = "UPDATE inventory SET quantity = %s, price = %s WHERE product_id = %s"
        params = (current_stock, current_price, product_id)
        execute_query(update_query, params) 
        messagebox.showinfo("Success", "Data updated successfully in the database")
        execute_query("DELETE FROM notify WHERE product_id = %s", (product_id,))
        stree_viewdt()
        tree_viewdt()  # Refresh the stock treeview

    clr()  # Clear fields after update

def clr():
    stock.delete(0, 'end')
    price.delete(0, 'end')
    p_id.config(text="")
    p_name.config(text="")
    c_name.config(text="")
    
def select_data(is_notification):
    clr()  # Clear fields before populating new data
    if is_notification:
        index = n_tree.selection()
        val = n_tree.item(index)
        r = val['values']
        f = execute_query("SELECT * FROM inventory WHERE product_id = %s", (r[0],))
    else:
        index = s_tree.selection()
        val = s_tree.item(index)
        r = val['values']
        f = execute_query("SELECT * FROM inventory WHERE product_id = %s", (r[0],))
    
    # Update labels and entries with selected product data
    p_id.config(text=f[0][0])
    p_name.config(text=f[0][1])
    c_name.config(text=f[0][2])
    stock.insert(0, f[0][3])
    price.insert(0, f[0][4])
    
    global p, s  # Store previous stock and price for comparison
    p = f[0][4]
    s = f[0][3]

def log_out_fn(root):
    if messagebox.askyesno('Confirmation', 'Do you want to log out?'):
        from clogin import run_login_page
        root.destroy()
        run_login_page()

def tree_viewdt():
    for row in n_tree.get_children():
        n_tree.delete(row)
    r = execute_query("SELECT product_id, reported_by, last_reported, no_of_out_of_stock, current_stock FROM notify")
    for row in r:
        n_tree.insert('', tk.END, values=row)

def stree_viewdt():
    for row in s_tree.get_children():
        s_tree.delete(row)
    r = execute_query("SELECT product_id, product_name, category, quantity, price FROM inventory")
    for row in r:
        s_tree.insert('', tk.END, values=row)

# Main Tkinter setup
def open_stock(name):
    global n_tree, s_tree, stock, price, p_id, p_name, c_name, p, s  # Declare variables as global
    root = tk.Tk()
    root.title("StockManager Dashboard")
    style = ttk.Style(root)
    root.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-dark")
    root.geometry('1278x668+0+0')
    root.resizable(0, 0)

    # Header
    tit_lab = Label(root, text="Stock Manager Panel", font=('inter', 25, 'bold'), bg="#111111", fg='white')
    tit_lab.place(x=0, y=0, relwidth=1)

    # Logout button
    lg_btn = ttk.Button(root, text="Logout", style='Accent.TButton', width=10, command=lambda: log_out_fn(root))
    lg_btn.place(x=1170, y=5)

    # Main frame for stock details
    d_frame = tk.Frame(root, width=900, height=567)
    d_frame.place(x=0, y=44)

    # Stock details header
    head_lbl = tk.Label(d_frame, text="Stock Details", font=(None, 16, 'bold'), fg='white')
    head_lbl.place(x=0, y=0, relwidth=1)

    # Notebook for tabs
    notebook = ttk.Notebook(d_frame)
    notebook.place(x=0, y=30, width=900, height=537)

    # Tabs for statistics and details
    tab_statistics = tk.Frame(notebook)
    notebook.add(tab_statistics, text="Notifications")
    tab_data_viz = tk.Frame(notebook)
    notebook.add(tab_data_viz, text="Quantity Details")

    # Notification Treeview setup
    hori = Scrollbar(tab_statistics, orient=tk.HORIZONTAL)
    veri = Scrollbar(tab_statistics, orient=tk.VERTICAL)
    n_tree = ttk.Treeview(tab_statistics, columns=('product_id', 'reported_by', 'last_reported', 'no_of_out_of_stock', 'current_stock'),
                        show='headings', yscrollcommand=veri.set, xscrollcommand=hori.set, height=20)

    veri.pack(side=tk.RIGHT, fill=tk.Y, pady=(10, 0))
    veri.config(command=n_tree.yview)

    # Adjusting the heading titles and column widths for notification treeview
    n_tree.heading('product_id', text='Product ID')
    n_tree.heading('reported_by', text='Reported By')
    n_tree.heading('last_reported', text='Last Reported')
    n_tree.heading('no_of_out_of_stock', text='Frequency')
    n_tree.heading('current_stock', text='Current Stock')
    n_tree.column('product_id', width=30)
    n_tree.column('reported_by', width=30)
    n_tree.column('last_reported', width=80)
    n_tree.column('no_of_out_of_stock', width=40)
    n_tree.column('current_stock', width=40)
    n_tree.pack(fill=tk.BOTH, pady=(10, 0), padx=(20, 0))
    n_tree.bind('<ButtonRelease-1>', lambda event: select_data(True))

    # Labels for product details
    pd = ttk.Label(root, text="Product Details", font=(None, 20, 'bold'))
    pd.place(x=980, y=90)
    a = ttk.Label(root, text="Product ID: ", font=(None, 14))
    a.place(x=920, y=160)
    c = ttk.Label(root, text="Category: ", font=(None, 14))
    c.place(x=920, y=300)
    b = ttk.Label(root, text="Product Name: ", font=(None, 14))
    b.place(x=920, y=230)
    d = ttk.Label(root, text="Stock: ", font=(None, 14))
    d.place(x=920, y=370)
    e = ttk.Label(root, text="Price: ", font=(None, 14))
    e.place(x=920, y=440)

    # Labels to display product information
    p_id = ttk.Label(root, text="", font=(None, 14))
    p_id.place(x=1070, y=160)
    p_name = ttk.Label(root, text="", font=(None, 14))
    p_name.place(x=1070, y=230)
    c_name = ttk.Label(root, text="", font=(None, 14))
    c_name.place(x=1070, y=300)

    # Entry fields for stock and price
    stock = ttk.Entry(root, font=(None, 14), width=10)
    stock.place(x=1070, y=370)
    price = ttk.Entry(root, font=(None, 14), width=10)
    price.place(x=1070, y=440)

    # Update button
    update_btn = ttk.Button(root, text="Update", cursor='hand2', width=15, style='Accent.TButton', command=up_ntf)
    update_btn.place(x=1020, y=550)

    # Stock Treeview setup
    hori = Scrollbar(tab_data_viz, orient=tk.HORIZONTAL)
    veri = Scrollbar(tab_data_viz, orient=tk.VERTICAL)
    s_tree = ttk.Treeview(tab_data_viz, columns=('product_id', 'product_name', 'category', 'quantity', 'price'),
                        show='headings', yscrollcommand=veri.set, xscrollcommand=hori.set, height=20)

    veri.pack(side=tk.RIGHT, fill=tk.Y, pady=(10, 0))
    veri.config(command=s_tree.yview)

    # Adjusting the heading titles and column widths for stock treeview
    s_tree.heading('product_id', text='Product ID')
    s_tree.heading('product_name', text='Product Name')
    s_tree.heading('category', text='Category')
    s_tree.heading('quantity', text='Quantity')
    s_tree.heading('price', text='Price')
    s_tree.column('product_id', width=30)
    s_tree.column('product_name', width=150)
    s_tree.column('category', width=100)
    s_tree.column('quantity', width=80)
    s_tree.column('price', width=80)
    s_tree.pack(fill=tk.BOTH, pady=(10, 0), padx=(20, 0))
    s_tree.bind('<ButtonRelease-1>', lambda event: select_data(False))
    sv_ttk.set_theme("dark")
    tree_viewdt()  # Initialize notification treeview
    stree_viewdt()  # Initialize stock treeview
    root.mainloop()
