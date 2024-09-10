import sqlite3
from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt

# Create a database connection
def connect_db():
    con = sqlite3.connect("finance.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS transactions 
                   (id INTEGER PRIMARY KEY, 
                    description TEXT, 
                    amount REAL, 
                    transaction_type TEXT, 
                    date TEXT)''')
    con.commit()
    con.close()

# Add a new transaction
def add_transaction():
    con = sqlite3.connect("finance.db")
    cur = con.cursor()
    cur.execute("INSERT INTO transactions (description, amount, transaction_type, date) VALUES (?, ?, ?, ?)", 
                (description_var.get(), amount_var.get(), transaction_type_var.get(), date_var.get()))
    con.commit()
    con.close()
    messagebox.showinfo("Success", "Transaction added successfully")
    view_transactions()

# View all transactions
def view_transactions():
    con = sqlite3.connect("finance.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()
    transaction_list.delete(0, END)
    for row in rows:
        transaction_list.insert(END, row)
    con.close()

# Select a transaction
def select_transaction(event):
    global selected_transaction
    index = transaction_list.curselection()[0]
    selected_transaction = transaction_list.get(index)

    description_var.set(selected_transaction[1])
    amount_var.set(selected_transaction[2])
    transaction_type_var.set(selected_transaction[3])
    date_var.set(selected_transaction[4])

# Update transaction data
def update_transaction():
    con = sqlite3.connect("finance.db")
    cur = con.cursor()
    cur.execute("UPDATE transactions SET description=?, amount=?, transaction_type=?, date=? WHERE id=?", 
                (description_var.get(), amount_var.get(), transaction_type_var.get(), date_var.get(), selected_transaction[0]))
    con.commit()
    con.close()
    messagebox.showinfo("Success", "Transaction updated successfully")
    view_transactions()

# Delete transaction data
def delete_transaction():
    con = sqlite3.connect("finance.db")
    cur = con.cursor()
    cur.execute("DELETE FROM transactions WHERE id=?", (selected_transaction[0],))
    con.commit()
    con.close()
    messagebox.showinfo("Success", "Transaction deleted successfully")
    view_transactions()

# Generate a bar chart for income and expenses
def show_graph():
    con = sqlite3.connect("finance.db")
    cur = con.cursor()
    cur.execute("SELECT transaction_type, SUM(amount) FROM transactions GROUP BY transaction_type")
    data = cur.fetchall()
    con.close()

    if data:
        labels = [row[0] for row in data]  # Labels for transaction types
        values = [row[1] for row in data]  # Corresponding total amounts
        
        plt.bar(labels, values, color=['green' if x == 'Income' else 'red' for x in labels])
        plt.title('Income vs Expenses')
        plt.ylabel('Amount')
        plt.xlabel('Transaction Type')
        plt.show()
    else:
        messagebox.showinfo("No Data", "No transactions to show.")

# Main GUI setup
root = Tk()
root.title("Personal Finance Tracker")
root.geometry("700x500")
root.configure(bg="#252a2e")

# Title Label
Label(root, text="Personal Finance Tracker", font=("Helvetica", 18, "bold"), bg="#252a2e", fg="white").pack(pady=20)

# Frame for input fields
input_frame = Frame(root, bg="#252a2e")
input_frame.pack(pady=10)

# Labels and Entry fields
Label(input_frame, text="Description", font=("Helvetica", 12), bg="#252a2e", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky=W)
description_var = StringVar()
Entry(input_frame, textvariable=description_var, width=30).grid(row=0, column=1, padx=10, pady=5)

Label(input_frame, text="Amount", font=("Helvetica", 12), bg="#252a2e", fg="white").grid(row=1, column=0, padx=10, pady=5, sticky=W)
amount_var = DoubleVar()
Entry(input_frame, textvariable=amount_var, width=30).grid(row=1, column=1, padx=10, pady=5)

Label(input_frame, text="Type (Income/Expense)", font=("Helvetica", 12), bg="#252a2e", fg="white").grid(row=2, column=0, padx=10, pady=5, sticky=W)
transaction_type_var = StringVar()
Entry(input_frame, textvariable=transaction_type_var, width=30).grid(row=2, column=1, padx=10, pady=5)

Label(input_frame, text="Date (YYYY-MM-DD)", font=("Helvetica", 12), bg="#252a2e", fg="white").grid(row=3, column=0, padx=10, pady=5, sticky=W)
date_var = StringVar()
Entry(input_frame, textvariable=date_var, width=30).grid(row=3, column=1, padx=10, pady=5)

# Frame for buttons
button_frame = Frame(root, bg="#252a2e")
button_frame.pack(pady=20)

# Row 1 buttons
add_btn = Button(button_frame, text="Add Transaction", command=add_transaction, width=15, bg="#4CAF50", fg="black", font=("Helvetica", 12))
add_btn.grid(row=0, column=0, padx=10, pady=10)

update_btn = Button(button_frame, text="Update Transaction", command=update_transaction, width=15, bg="#2196F3", fg="black", font=("Helvetica", 12))
update_btn.grid(row=0, column=1, padx=10, pady=10)

delete_btn = Button(button_frame, text="Delete Transaction", command=delete_transaction, width=15, bg="#F44336", fg="black", font=("Helvetica", 12))
delete_btn.grid(row=0, column=2, padx=10, pady=10)

# Row 2 buttons
view_btn = Button(button_frame, text="View All Transactions", command=view_transactions, width=15, bg="#FF9800", fg="black", font=("Helvetica", 12))
view_btn.grid(row=1, column=0, padx=10, pady=10)

graph_btn = Button(button_frame, text="Show Graph", command=show_graph, width=15, bg="#673AB7", fg="black", font=("Helvetica", 12))
graph_btn.grid(row=1, column=1, padx=10, pady=10)

close_btn = Button(button_frame, text="Close", command=root.quit, width=15, bg="#9E9E9E", fg="black", font=("Helvetica", 12))
close_btn.grid(row=1, column=2, padx=10, pady=10)

# Listbox to show records
listbox_frame = Frame(root, bg="black")
listbox_frame.pack(pady=10)

transaction_list = Listbox(listbox_frame, height=10, width=80, font=("Helvetica", 12), bg="black", bd=0, fg="white")
transaction_list.pack(padx=20, pady=5)
transaction_list.bind('<<ListboxSelect>>', select_transaction)

# Connect to the database and run the app
connect_db()
view_transactions()
root.mainloop()
