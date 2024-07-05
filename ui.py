import tkinter as tk
import requests
from tkinter import messagebox

class CanteenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Canteen Purchases")

        # Labels
        tk.Label(root, text="Name:").grid(row=0, column=0, sticky='w')
        tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky='w')
        tk.Label(root, text="Time (HH:MM):").grid(row=2, column=0, sticky='w')
        tk.Label(root, text="Item:").grid(row=3, column=0, sticky='w')
        tk.Label(root, text="Quantity:").grid(row=4, column=0, sticky='w')
        tk.Label(root, text="Payment (INR):").grid(row=5, column=0, sticky='w')
        tk.Label(root, text="Role (student/faculty/worker):").grid(row=6, column=0, sticky='w')

        # Entry fields
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=1, column=1)
        self.time_entry = tk.Entry(root)
        self.time_entry.grid(row=2, column=1)
        self.item_entry = tk.Entry(root)
        self.item_entry.grid(row=3, column=1)
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row=4, column=1)
        self.payment_entry = tk.Entry(root)
        self.payment_entry.grid(row=5, column=1)
        self.role_entry = tk.Entry(root)
        self.role_entry.grid(row=6, column=1)

        # Submit button
        tk.Button(root, text="Submit", command=self.submit_data).grid(row=7, column=0, columnspan=2, pady=10)

    def submit_data(self):
        # Get data from entry fields
        name = self.name_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        item = self.item_entry.get()
        quantity = int(self.quantity_entry.get())
        payment = float(self.payment_entry.get())
        role = self.role_entry.get()

        # Prepare data payload to send to server
        data = {
            'name': name,
            'date': date,
            'time': time,
            'item': item,
            'quantity': quantity,
            'payment': payment,
            'role': role,
            'location': 'Canteen'  # Include the hardcoded location field
        }

        # Get JWT token from the server
        try:
            token_response = requests.get('http://localhost:8080/api/token')
            if token_response.status_code == 200:
                token = token_response.json()['token']
            else:
                messagebox.showerror("Error", f"Failed to get token: {token_response.status_code}")
                return
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error connecting to server for token: {e}")
            return

        # Send data to server
        try:
            response = requests.post('http://localhost:8080/api/purchase', json=data, headers={'Authorization': f'Bearer {token}'})
            if response.status_code == 200:
                messagebox.showinfo("Success", "Data submitted successfully!")
                self.clear_entries()  # Clear entry fields after successful submission
            else:
                messagebox.showerror("Error", f"Failed to submit data: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error connecting to server: {e}")

    def clear_entries(self):
        # Clear all entry fields
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.item_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.payment_entry.delete(0, tk.END)
        self.role_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CanteenApp(root)
    root.mainloop()
