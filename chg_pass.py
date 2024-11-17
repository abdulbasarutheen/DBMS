import customtkinter as ctk
from tkinter import messagebox, ttk
from db_cn import execute_query
from tkinter import *
import tkinter as tk

def change_pass(root, user_id):
    change_pass_win = Toplevel(root)
    change_pass_win.title("Change Password")
    change_pass_win.geometry("400x350")
    
    Label(change_pass_win, text="Current Password:", font=(None, 12)).pack(pady=10)
    current_pass_entry = ttk.Entry(change_pass_win, show="*")
    current_pass_entry.pack(pady=5)

    Label(change_pass_win, text="New Password:", font=(None, 12)).pack(pady=10)
    new_pass_entry = ttk.Entry(change_pass_win, show="*")
    new_pass_entry.pack(pady=5)

    Label(change_pass_win, text="Confirm New Password:", font=(None, 12)).pack(pady=10)
    confirm_pass_entry = ttk.Entry(change_pass_win, show="*")
    confirm_pass_entry.pack(pady=5)

    def change_password():
        current_password = current_pass_entry.get()
        new_password = new_pass_entry.get()
        confirm_password = confirm_pass_entry.get()

        result = execute_query("SELECT password FROM employee_credentials WHERE emp_id = %s", (user_id,))
        if result and result[0][0] != current_password:
            messagebox.showerror("Error", "Current password is incorrect!")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New Password and Confirm Password do not match!")
            return

        execute_query("UPDATE employee_credentials SET password = %s WHERE emp_id = %s", (new_password, user_id))
        messagebox.showinfo("Success", "Password changed successfully!")
        change_pass_win.destroy()

    change_button = ttk.Button(change_pass_win, text="Change Password", style='Accent.TButton', command=change_password)
    change_button.pack(pady=20)
