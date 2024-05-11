import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class Inventory:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            name TEXT PRIMARY KEY,
                            price REAL,
                            quantity INTEGER)''')
        self.connection.commit()

    def add_product(self, product):
        self.cursor.execute('''INSERT INTO products VALUES (?, ?, ?)''',
                            (product.name, product.price, product.quantity))
        self.connection.commit()

    def remove_product(self, product_name):
        self.cursor.execute('''DELETE FROM products WHERE name=?''', (product_name,))
        self.connection.commit()

    def get_products(self):
        self.cursor.execute('''SELECT * FROM products''')
        return self.cursor.fetchall()

class Order:
    def __init__(self):
        self.products_ordered = []

    def add_to_order(self, product, quantity):
        self.products_ordered.append((product, quantity))

    def clear_order(self):
        self.products_ordered = []

    def generate_receipt(self):
        receipt = "Order Receipt\n"
        receipt += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        receipt += "Products:\n"
        total_price = 0
        for product, quantity in self.products_ordered:
            receipt += f"{product.name} x{quantity}: ${product.price * quantity:.2f}\n"
            total_price += product.price * quantity
        receipt += f"\nTotal Price: ${total_price:.2f}"
        return receipt

class InventoryManagementSystemApp:
    def __init__(self, root, inventory):
        self.root = root
        self.inventory = inventory
        self.order = Order()

        self.product_name_var = tk.StringVar()
        self.product_price_var = tk.DoubleVar()
        self.product_quantity_var = tk.IntVar()

        self.create_gui()

    def create_gui(self):
        self.root.title("FreshMart Inventory Management System")

        # Create a menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create a File menu with options for adding and removing products
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Add Product", command=self.add_product)
        file_menu.add_command(label="Remove Product", command=self.remove_product)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Create a Orders menu with options for managing orders
        orders_menu = tk.Menu(menubar, tearoff=False)
        orders_menu.add_command(label="Add to Order", command=self.add_to_order)
        orders_menu.add_command(label="Clear Order", command=self.clear_order)
        orders_menu.add_command(label="Generate Receipt", command=self.generate_receipt)
        menubar.add_cascade(label="Orders", menu=orders_menu)

        # Create a Help menu with an about option
        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Create notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Products tab
        products_tab = ttk.Frame(notebook)
        notebook.add(products_tab, text='Products')

        tk.Label(products_tab, text="Product Name:").pack()
        tk.Entry(products_tab, textvariable=self.product_name_var).pack()

        tk.Label(products_tab, text="Price:").pack()
        tk.Entry(products_tab, textvariable=self.product_price_var).pack()

        tk.Label(products_tab, text="Quantity:").pack()
        tk.Entry(products_tab, textvariable=self.product_quantity_var).pack()

        tk.Button(products_tab, text="Add Product", command=self.add_product).pack()
        tk.Button(products_tab, text="Remove Product", command=self.remove_product).pack()

        # Orders tab
        orders_tab = ttk.Frame(notebook)
        notebook.add(orders_tab, text='Orders')

        self.order_text = tk.Text(orders_tab, wrap=tk.WORD)
        self.order_text.pack(expand=True, fill=tk.BOTH)

    def add_product(self):
        name = self.product_name_var.get()
        price = self.product_price_var.get()
        quantity = self.product_quantity_var.get()

        product = Product(name, price, quantity)
        self.inventory.add_product(product)
        messagebox.showinfo("Success", f"Added product: {name}, Price: {price}, Quantity: {quantity}")

    def remove_product(self):
        name = self.product_name_var.get()
        self.inventory.remove_product(name)
        messagebox.showinfo("Success", f"Removed product: {name}")

    def add_to_order(self):
        name = self.product_name_var.get()
        quantity = self.product_quantity_var.get()

        products = self.inventory.get_products()
        for product in products:
            if product[0] == name:
                self.order.add_to_order(Product(product[0], product[1], product[2]), quantity)
                messagebox.showinfo("Success", f"Added {quantity} {name} to order")
                return
        messagebox.showerror("Error", "Product not found")

    def clear_order(self):
        self.order.clear_order()
        self.order_text.delete(1.0, tk.END)

    def generate_receipt(self):
        if not self.order.products_ordered:
            messagebox.showwarning("Warning", "Order is empty")
            return
        receipt = self.order.generate_receipt()
        self.order_text.delete(1.0, tk.END)
        self.order_text.insert(tk.END, receipt)

    def show_about(self):
        messagebox.showinfo("About", "FreshMart Inventory Management System\nVersion 1.0")

if __name__ == "__main__":
    # Initialize inventory with SQLite database
    inventory = Inventory("inventory.db")

    # Create root window
    root = tk.Tk()

    # Create the application
    app = InventoryManagementSystemApp(root, inventory)

    # Start the application
    root.mainloop()