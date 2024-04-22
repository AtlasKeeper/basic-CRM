import sqlite3
import tkinter as tk
from tkinter import messagebox

# Create a new window
window = tk.Tk()
window.title("CRM Software")

# Create labels and entry fields for customer info
labels = ["Name", "Email", "Phone"]
entries = []

for i, label in enumerate(labels):
    tk.Label(window, text=label).grid(row=i)
    entries.append(tk.Entry(window))
    entries[i].grid(row=i, column=1)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('customer_info.db')
c = conn.cursor()

# Create tables for the customer info and meetings
c.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        name TEXT,
        email TEXT,
        phone TEXT
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS meetings (
        customer_name TEXT,
        date TEXT,
        notes TEXT
    )
''')

# Function to save customer info
def save_info():
    info = [entry.get() for entry in entries]
    c.execute('INSERT INTO customers VALUES (?, ?, ?)', info)
    conn.commit()
    messagebox.showinfo("Saved", "Customer information has been saved successfully.")

# Function to show all customer info
def show_all():
    c.execute('SELECT * FROM customers')
    data = c.fetchall()
    info = "\n".join(", ".join(map(str, row)) for row in data)
    messagebox.showinfo("All Customers", info)

# Function to manage meetings
def manage_meetings():
    # Create a new window for managing meetings
    meetings_window = tk.Toplevel(window)
    meetings_window.title("Manage Meetings")

    # Create labels and entry fields for meeting info
    meeting_labels = ["Customer Name", "Date", "Notes"]
    meeting_entries = []

    for i, label in enumerate(meeting_labels):
        tk.Label(meetings_window, text=label).grid(row=i)
        meeting_entries.append(tk.Entry(meetings_window))
        meeting_entries[i].grid(row=i, column=1)

    # Function to save meeting info
    def save_meeting():
        meeting_info = [entry.get() for entry in meeting_entries]
        c.execute('INSERT INTO meetings VALUES (?, ?, ?)', meeting_info)
        conn.commit()
        messagebox.showinfo("Saved", "Meeting information has been saved successfully.")

    # Function to show all meetings
    def show_all_meetings():
        c.execute('SELECT * FROM meetings')
        data = c.fetchall()
        info = "\n".join(", ".join(map(str, row)) for row in data)
        messagebox.showinfo("All Meetings", info)

    # Create a save button
    save_meeting_button = tk.Button(meetings_window, text="Save Meeting", command=save_meeting)
    save_meeting_button.grid(row=len(meeting_labels), column=1)

    # Create a show all button
    show_all_meetings_button = tk.Button(meetings_window, text="Show All Meetings", command=show_all_meetings)
    show_all_meetings_button.grid(row=len(meeting_labels)+1, column=1)

# Create a save button
save_button = tk.Button(window, text="Save", command=save_info)
save_button.grid(row=len(labels), column=1)

# Create a show all button
show_all_button = tk.Button(window, text="Show All", command=show_all)
show_all_button.grid(row=len(labels)+1, column=1)

# Create a manage meetings button
manage_meetings_button = tk.Button(window, text="Manage Meetings", command=manage_meetings)
manage_meetings_button.grid(row=len(labels)+2, column=1)

# Run the application
window.mainloop()

# Close the connection to the database when the application is closed
conn.close()
