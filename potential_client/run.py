import sqlite3
import tkinter as tk
from tkinter import messagebox

# Create a new window
window = tk.Tk()
window.title("CRM Software")

# Create labels and entry fields for customer info
labels = [
    "Name", "Email", "Phone", "Mailing Address", "Age", "Gender", "Occupation", "Income Level", 
    "Education Level", "Marital Status", "Family Size", "Risk Tolerance", "Investment Objectives", 
    "Time Horizon for Investments", "Preferred Investment Vehicles", "Previous Investment Experience", 
    "Net Worth", "Income Sources", "Debts and Liabilities", "Assets", "Preferred Method of Communication", 
    "Frequency of Communication", "Topics of Interest", "History of Interactions", "Feedback or Comments", 
    "Referral Sources", "Legal Documentation", "Hobbies or Interests", "Social Media Profiles", 
    "Online Behavior", "Market Trends Interest", "News Sources Followed", "Track Portfolio Performance", 
    "Behavior Analytics"
]
entries = []

for i, label in enumerate(labels):
    tk.Label(window, text=label).grid(row=i)
    entries.append(tk.Entry(window))
    entries[i].grid(row=i, column=1)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('customer_info.db')
c = conn.cursor()

# Create a table for the customer info
c.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        name TEXT,
        email TEXT,
        phone TEXT,
        mailing_address TEXT,
        age INTEGER,
        gender TEXT,
        occupation TEXT,
        income_level REAL,
        education_level TEXT,
        marital_status TEXT,
        family_size INTEGER,
        risk_tolerance TEXT,
        investment_objectives TEXT,
        time_horizon_for_investments TEXT,
        preferred_investment_vehicles TEXT,
        previous_investment_experience TEXT,
        net_worth REAL,
        income_sources TEXT,
        debts_and_liabilities REAL,
        assets TEXT,
        preferred_method_of_communication TEXT,
        frequency_of_communication TEXT,
        topics_of_interest TEXT,
        history_of_interactions TEXT,
        feedback_or_comments TEXT,
        referral_sources TEXT,
        legal_documentation TEXT,
        hobbies_or_interests TEXT,
        social_media_profiles TEXT,
        online_behavior TEXT,
        market_trends_interest TEXT,
        news_sources_followed TEXT,
        track_portfolio_performance TEXT,
        behavior_analytics TEXT
    )
''')

# Function to save customer info
def save_info():
    info = [entry.get() for entry in entries]
    c.execute('''
        INSERT INTO customers VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    ''', info)
    conn.commit()
    messagebox.showinfo("Saved", "Customer information has been saved successfully.")

# Function to show all customer info
def show_all():
    c.execute('SELECT * FROM customers')
    data = c.fetchall()
    info = "\\n".join(", ".join(map(str, row)) for row in data)
    messagebox.showinfo("All Customers", info)

# Function to search for a customer
def search_customer():
    search_window = tk.Toplevel(window)
    search_window.title("Search Customer")

    # Create label and entry field for search term
    tk.Label(search_window, text="Name").grid(row=0)
    search_entry = tk.Entry(search_window)
    search_entry.grid(row=0, column=1)

    # Function to perform search
    def perform_search():
        name = search_entry.get()
        c.execute('SELECT * FROM customers WHERE name = ?', (name,))
        data = c.fetchall()
        info = "\\n".join(", ".join(map(str, row)) for row in data)
        messagebox.showinfo("Search Results", info)

    # Create a search button
    search_button = tk.Button(search_window, text="Search", command=perform_search)
    search_button.grid(row=1, column=1)

# Create a save button
save_button = tk.Button(window, text="Save", command=save_info)
save_button.grid(row=len(labels), column=1)

# Create a show all button
show_all_button = tk.Button(window, text="Show All", command=show_all)
show_all_button.grid(row=len(labels)+1, column=1)

# Create a search button
search_button = tk.Button(window, text="Search", command=search_customer)
search_button.grid(row=len(labels)+2, column=1)

# Run the application
window.mainloop()

# Close the connection to the database when the application is closed
conn.close()
