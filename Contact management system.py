import tkinter as tk  # Import tkinter for GUI
from tkinter import messagebox, simpledialog  # Import messagebox and simpledialog for interactions
import mysql.connector  # Import mysql.connector to connect to MySQL database

# Database connection setup
def connect_db():
    """Establish a connection to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",  # Hostname where MySQL server is running
        user="root",  # Replace with your MySQL username
        password="Avinash@9199",  # Replace with your MySQL password
        database="contacts_db"  # Name of the database to connect to
    )

# Function to add a contact
def add_contact():
    """Add a new contact to the database."""
    name = name_entry.get()  # Get the name from the entry field
    phone = phone_entry.get()  # Get the phone number from the entry field
    email = email_entry.get()  # Get the email from the entry field
    address = address_entry.get()  # Get the address from the entry field

    if not name or not phone:  # Check for empty name or phone
        messagebox.showwarning("Input Error", "Name and Phone cannot be empty!")
        return

    conn = connect_db()  # Establish a connection to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL queries

    try:
        # Execute the INSERT statement to add the contact
        cursor.execute(
            "INSERT INTO Contacts (Name, Phone, Email, Address) VALUES (%s, %s, %s, %s)",
            (name, phone, email, address),
        )
        conn.commit()  # Commit the transaction to the database
        messagebox.showinfo("Success", "Contact added successfully!")  # Show success message
        display_contacts()  # Refresh the displayed contacts
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Phone number must be unique!")  # Show error if phone is not unique
    finally:
        cursor.close()  # Close the cursor
        conn.close()  # Close the database connection

# Function to delete a contact
def delete_contact():
    """Delete a contact from the database."""
    name_to_delete = simpledialog.askstring("Delete Contact", "Enter the name of the contact to delete:")
    if name_to_delete:
        conn = connect_db()  # Establish a connection to the database
        cursor = conn.cursor()  # Create a cursor to execute SQL queries

        # Execute the DELETE statement to remove the contact
        cursor.execute("DELETE FROM Contacts WHERE Name = %s", (name_to_delete,))
        if cursor.rowcount == 0:
            messagebox.showwarning("Delete Error", "Contact not found!")  # Show warning if contact not found
        else:
            conn.commit()  # Commit the transaction to the database
            messagebox.showinfo("Success", "Contact deleted successfully!")  # Show success message

        cursor.close()  # Close the cursor
        conn.close()  # Close the database connection
        display_contacts()  # Refresh the displayed contacts

# Function to display all contacts
def display_contacts():
    """Fetch and display all contacts from the database."""
    conn = connect_db()  # Establish a connection to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL queries
    cursor.execute("SELECT * FROM Contacts")  # Execute the SELECT statement to get all contacts
    records = cursor.fetchall()  # Fetch all records from the query
    cursor.close()  # Close the cursor
    conn.close()  # Close the database connection

    # Clear previous records displayed
    for widget in contact_frame.winfo_children():
        widget.destroy()

    # Display fetched records in the contact frame
    for record in records:
        contact_label = tk.Label(contact_frame, text=record, bg="lightblue", font=("Arial", 10, "bold"))  # Enhanced display
        contact_label.pack(pady=5)  # Add padding for better spacing

# Function to search contacts
def search_contact():
    """Search for contacts by name or phone number."""
    search_term = search_entry.get()  # Get the search term from the entry field
    conn = connect_db()  # Establish a connection to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL queries
    # Execute the SELECT statement to search for contacts
    cursor.execute(
        "SELECT * FROM Contacts WHERE Name LIKE %s OR Phone LIKE %s",
        ('%' + search_term + '%', '%' + search_term + '%')  # Use wildcards for partial matches
    )
    records = cursor.fetchall()  # Fetch all matching records
    cursor.close()  # Close the cursor
    conn.close()  # Close the database connection

    # Clear previous records displayed
    for widget in contact_frame.winfo_children():
        widget.destroy()

    # Display fetched records in the contact frame
    for record in records:
        contact_label = tk.Label(contact_frame, text=record, bg="lightgreen", font=("Arial", 10, "bold"))  # Enhanced display
        contact_label.pack(pady=5)  # Add padding for better spacing

# Create main window
root = tk.Tk()  # Initialize the main window
root.title("Contact Management System")  # Set the title of the window
root.geometry("500x400")  # Set the window size

# Input fields for contact information
tk.Label(root, text="Name", font=("Arial", 12)).grid(row=0, padx=10, pady=5)  # Label for Name
tk.Label(root, text="Phone", font=("Arial", 12)).grid(row=1, padx=10, pady=5)  # Label for Phone
tk.Label(root, text="Email", font=("Arial", 12)).grid(row=2, padx=10, pady=5)  # Label for Email
tk.Label(root, text="Address", font=("Arial", 12)).grid(row=3, padx=10, pady=5)  # Label for Address

# Entry fields for user input
name_entry = tk.Entry(root)  # Entry for Name
phone_entry = tk.Entry(root)  # Entry for Phone
email_entry = tk.Entry(root)  # Entry for Email
address_entry = tk.Entry(root)  # Entry for Address

# Place entry fields in the grid
name_entry.grid(row=0, column=1)  
phone_entry.grid(row=1, column=1)  
email_entry.grid(row=2, column=1)  
address_entry.grid(row=3, column=1)  

# Add Contact button to trigger the add_contact function
tk.Button(root, text="Add Contact", command=add_contact, bg="blue", fg="white").grid(row=4, column=1, pady=10)  # Styled button

# Delete Contact button to trigger the delete_contact function
tk.Button(root, text="Delete Contact", command=delete_contact, bg="red", fg="white").grid(row=4, column=2, pady=10)  # Styled button

# Search box for finding contacts
tk.Label(root, text="Search", font=("Arial", 12)).grid(row=5, padx=10, pady=5)  # Label for Search
search_entry = tk.Entry(root)  # Entry for search term
search_entry.grid(row=5, column=1)  # Place search entry in the grid
# Search button to trigger the search_contact function
tk.Button(root, text="Search", command=search_contact, bg="green", fg="white").grid(row=5, column=2, pady=10)  # Styled button

# Frame to display contacts
contact_frame = tk.Frame(root)  # Create a frame for displaying contacts
contact_frame.grid(row=6, columnspan=3, padx=10, pady=10)  # Place the frame in the grid

# Run the main loop to display the GUI
root.mainloop()  # Start the tkinter event loop
