import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
import sv_ttk
from db_cn import execute_query
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def sta_rep(root):

    d_frame = tk.Frame(root, width=1070, height=567)
    d_frame.place(x=225, y=100)
    style = ttk.Style(d_frame)
    style.theme_use("forest-dark")

    # Header label
    head_lbl = tk.Label(d_frame, text="Statistical Report", font=(None, 16, 'bold'), fg='white')
    head_lbl.place(x=0, y=0, relwidth=1)

    # Notebook (tabs) inside d_frame
    notebook = ttk.Notebook(d_frame)
    notebook.place(x=0, y=30, width=1070, height=537)

    # Statistics Tab
    tab_data_viz = tk.Frame(notebook)
    notebook.add(tab_data_viz, text="Data Visualization")

    # Sales by Date
    query = "SELECT sale_date, total_amount FROM sales"
    data = execute_query(query, ())
    df = pd.DataFrame(data, columns=["Sale Date", "Total Amount"])
    df['Sale Date'] = pd.to_datetime(df['Sale Date'])
    sales_by_date = df.groupby(df['Sale Date'].dt.date)['Total Amount'].sum()

    # Create Line Chart for Sales by Date
    fig1 = Figure(figsize=(3, 3.5), facecolor="#1f1f1f")
    ax_1 = fig1.add_subplot()
    ax_1.set_facecolor("#1f1f1f")
    ax_1.fill_between(x=sales_by_date.index, y1=sales_by_date.values, alpha=0.7)
    ax_1.tick_params(labelsize=7, colors="white")
    fig1.autofmt_xdate()
    ax_1.plot(sales_by_date.index, sales_by_date.values, color="deepskyblue")
    ax_1.grid(visible=True, alpha=0.3)
    ax_1.set_title("Sales by Date", color="white", fontsize=12)

    # Data Visualization Tab for Sales by Date
    canvas = FigureCanvasTkAgg(figure=fig1, master=tab_data_viz)
    canvas.draw()
    canvas.get_tk_widget().place(x=50, y=60)

    # Query to fetch payment methods
    query_payment_method = "SELECT payment_method FROM sales"
    payment_data = execute_query(query_payment_method, ())
    payment_df = pd.DataFrame(payment_data, columns=["Payment Method"])
    payment_counts = payment_df['Payment Method'].value_counts()

    # Create Pie Chart for Payment Method Distribution
    fig2 = Figure(figsize=(3, 3.5), facecolor="#1f1f1f")
    ax_2 = fig2.add_subplot()
    dark_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    wedges, texts, autotexts = ax_2.pie(payment_counts, 
                                        labels=payment_counts.index, 
                                        colors=dark_colors,
                                        startangle=90, 
                                        autopct='%1.1f%%',
                                        textprops=dict(color='white'))
    ax_2.axis('equal')
    ax_2.set_title("Payment Method Distribution", color="white", fontsize=12)

    # Data Visualization Tab for Pie Chart
    canvas_pie = FigureCanvasTkAgg(figure=fig2, master=tab_data_viz)
    canvas_pie.draw()
    canvas_pie.get_tk_widget().place(x=380, y=60)

    # Query to fetch sales by employees
    query_top_employees = """
    SELECT emp_id, SUM(total_amount) as total_sales 
    FROM sales 
    GROUP BY emp_id 
    ORDER BY total_sales DESC 
    LIMIT 5
    """

    # Execute query to get top employees
    top_employees_data = execute_query(query_top_employees, ())

    # Convert the data to a pandas DataFrame
    top_employees_df = pd.DataFrame(top_employees_data, columns=["Employee ID", "Total Sales"])

    # Create a horizontal bar graph
    fig3 = Figure(figsize=(3, 3.5), facecolor="#1f1f1f")  # Adjust size for better visibility
    ax_3 = fig3.add_subplot()
    ax_3.barh(top_employees_df["Employee ID"].astype(str), top_employees_df["Total Sales"], color="deepskyblue")

    # Set labels and title
    ax_3.set_xlabel("Total Sales", color="white")
    ax_3.set_ylabel("Employee ID", color="white")
    ax_3.set_title("Top 3 Employees by Sales", color="white")
    ax_3.set_facecolor("#1f1f1f")
    # Adjust tick parameters
    ax_3.tick_params(axis='x', colors="white")
    ax_3.tick_params(axis='y', colors="white")

    # Data Visualization Tab for Bar Graph
    canvas_bar = FigureCanvasTkAgg(figure=fig3, master=tab_data_viz)
    canvas_bar.draw()
    canvas_bar.get_tk_widget().place(x=700, y=60)
    
    sv_ttk.set_theme("dark")

