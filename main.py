"""
JK's Boutique and Kid's Wear Application
A desktop application for managing boutique inventory and sales
Author: Kiwumulo Joanah
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


class Product:
    """Product class to represent inventory items"""
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['product_id'], data['name'], data['price'], data['quantity'])


class User:
    """User class to represent registered users"""
    def __init__(self, username, password, full_name, email):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
    
    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'full_name': self.full_name,
            'email': self.email
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['username'], data['password'], data['full_name'], data['email'])


class DatabaseManager:
    """Class to manage SQLite database operations"""
    def __init__(self, db_name='boutique.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.initialize_database()
    
    def initialize_database(self):
        """Create database connection and tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        # Create products table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create receipts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS receipts (
                receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_number INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                filename TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create receipt_items table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS receipt_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (receipt_id) REFERENCES receipts (receipt_id),
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )
        ''')
        
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    # Product operations
    def add_product(self, name, price, quantity):
        """Add a new product to the database"""
        self.cursor.execute('''
            INSERT INTO products (name, price, quantity)
            VALUES (?, ?, ?)
        ''', (name, price, quantity))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_all_products(self):
        """Get all products from the database"""
        self.cursor.execute('SELECT product_id, name, price, quantity FROM products ORDER BY product_id')
        return self.cursor.fetchall()
    
    def get_product(self, product_id):
        """Get a specific product by ID"""
        self.cursor.execute('SELECT product_id, name, price, quantity FROM products WHERE product_id = ?', (product_id,))
        return self.cursor.fetchone()
    
    def update_product(self, product_id, name, price, quantity):
        """Update a product"""
        self.cursor.execute('''
            UPDATE products 
            SET name = ?, price = ?, quantity = ?, updated_at = CURRENT_TIMESTAMP
            WHERE product_id = ?
        ''', (name, price, quantity, product_id))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def delete_product(self, product_id):
        """Delete a product"""
        self.cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_low_stock_count(self, threshold=10):
        """Get count of products with low stock"""
        self.cursor.execute('SELECT COUNT(*) FROM products WHERE quantity < ?', (threshold,))
        return self.cursor.fetchone()[0]
    
    def get_total_inventory_value(self):
        """Calculate total inventory value"""
        self.cursor.execute('SELECT SUM(price * quantity) FROM products')
        result = self.cursor.fetchone()[0]
        return result if result else 0
    
    # User operations
    def register_user(self, username, password, full_name, email):
        """Register a new user"""
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password, full_name, email)
                VALUES (?, ?, ?, ?)
            ''', (username, password, full_name, email))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists
    
    def get_user(self, username):
        """Get user by username"""
        self.cursor.execute('SELECT username, password, full_name, email FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()
    
    def username_exists(self, username):
        """Check if username already exists"""
        self.cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()[0] > 0
    
    # Receipt operations
    def save_receipt(self, receipt_number, total_amount, filename, items):
        """Save receipt and its items"""
        # Insert receipt
        self.cursor.execute('''
            INSERT INTO receipts (receipt_number, total_amount, filename)
            VALUES (?, ?, ?)
        ''', (receipt_number, total_amount, filename))
        receipt_id = self.cursor.lastrowid
        
        # Insert receipt items
        for item in items:
            self.cursor.execute('''
                INSERT INTO receipt_items (receipt_id, product_id, product_name, price, quantity, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (receipt_id, item['product_id'], item['name'], item['price'], item['quantity'], item['subtotal']))
        
        self.conn.commit()
        return receipt_id
    
    def get_next_receipt_number(self):
        """Get the next receipt number"""
        self.cursor.execute('SELECT MAX(receipt_number) FROM receipts')
        result = self.cursor.fetchone()[0]
        return (result + 1) if result else 1
    
    def get_receipt_history(self, limit=50):
        """Get recent receipt history"""
        self.cursor.execute('''
            SELECT receipt_id, receipt_number, total_amount, filename, created_at
            FROM receipts
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()


class DataManager:
    """Legacy wrapper for backward compatibility"""
    def __init__(self, filename='inventory.json', users_filename='users.json'):
        self.db = DatabaseManager()
        # Keep old filenames for reference but don't use them
        self.filename = filename
        self.users_filename = users_filename
    
    def get_all_products(self):
        """Get all products as Product objects"""
        products = self.db.get_all_products()
        return [Product(p[0], p[1], p[2], p[3]) for p in products]
    
    def get_product(self, product_id):
        """Get a specific product"""
        product = self.db.get_product(product_id)
        if product:
            return Product(product[0], product[1], product[2], product[3])
        return None
    
    def add_product(self, product):
        """Add a product"""
        self.db.add_product(product.name, product.price, product.quantity)
    
    def update_product(self, product_id, name, price, quantity):
        """Update a product"""
        return self.db.update_product(product_id, name, price, quantity)
    
    def delete_product(self, product_id):
        """Delete a product"""
        return self.db.delete_product(product_id)
    
    def get_next_id(self):
        """Get next product ID (not needed with auto-increment but kept for compatibility)"""
        products = self.db.get_all_products()
        if not products:
            return 1
        return max(p[0] for p in products) + 1
    
    def register_user(self, user):
        """Register a new user"""
        return self.db.register_user(user.username, user.password, user.full_name, user.email)
    
    def get_user(self, username):
        """Get user by username"""
        user_data = self.db.get_user(username)
        if user_data:
            return User(user_data[0], user_data[1], user_data[2], user_data[3])
        return None
    
    def username_exists(self, username):
        """Check if username exists"""
        return self.db.username_exists(username)


class ReceiptGenerator:
    """Class to generate professional PDF invoices/receipts"""
    @staticmethod
    def get_receipts_folder():
        """Get the receipts folder path, works with PyInstaller"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = os.path.dirname(sys.executable)
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        receipts_folder = os.path.join(base_path, 'receipts')
        
        # Create receipts folder if it doesn't exist
        if not os.path.exists(receipts_folder):
            os.makedirs(receipts_folder)
        
        return receipts_folder
    
    @staticmethod
    def generate_receipt(items, total, receipt_number):
        """Generate a professional invoice PDF with company branding"""
        # Create receipts folder and get full path
        receipts_folder = ReceiptGenerator.get_receipts_folder()
        filename = f"invoice_{receipt_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        full_path = os.path.join(receipts_folder, filename)
        
        c = canvas.Canvas(full_path, pagesize=letter)
        width, height = letter
        
        # Draw border
        c.setStrokeColorRGB(0.2, 0.2, 0.2)
        c.setLineWidth(2)
        c.rect(0.5*inch, 0.5*inch, width - 1*inch, height - 1*inch)
        
        # Header - Company Name
        c.setFillColorRGB(0.17, 0.24, 0.31)  # Dark blue-gray
        c.rect(0.5*inch, height - 1.5*inch, width - 1*inch, 1*inch, fill=True, stroke=False)
        
        c.setFillColorRGB(1, 1, 1)  # White text
        c.setFont("Helvetica-Bold", 24)
        c.drawString(1*inch, height - 1.2*inch, "JK's Boutique & Kid's Wear")
        
        c.setFont("Helvetica", 10)
        c.drawString(1*inch, height - 1.4*inch, "Quality Children's Clothing | Kampala, Uganda")
        
        # Invoice Title
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(1*inch, height - 2*inch, "INVOICE")
        
        # Invoice Details Box
        c.setFont("Helvetica-Bold", 11)
        c.drawString(4.5*inch, height - 2*inch, "Invoice #:")
        c.drawString(4.5*inch, height - 2.25*inch, "Date:")
        c.drawString(4.5*inch, height - 2.5*inch, "Time:")
        
        c.setFont("Helvetica", 11)
        c.drawString(5.5*inch, height - 2*inch, f"{receipt_number:05d}")
        c.drawString(5.5*inch, height - 2.25*inch, datetime.now().strftime('%Y-%m-%d'))
        c.drawString(5.5*inch, height - 2.5*inch, datetime.now().strftime('%H:%M:%S'))
        
        # Items Table Header
        y_position = height - 3*inch
        c.setFillColorRGB(0.17, 0.24, 0.31)
        c.rect(0.75*inch, y_position - 0.05*inch, width - 1.5*inch, 0.3*inch, fill=True, stroke=False)
        
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(1*inch, y_position, "ITEM")
        c.drawString(3.5*inch, y_position, "QTY")
        c.drawString(4.5*inch, y_position, "PRICE")
        c.drawString(5.7*inch, y_position, "SUBTOTAL")
        
        # Items
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 10)
        y_position -= 0.35*inch
        
        item_count = 0
        for item in items:
            item_count += 1
            # Alternate row colors
            if item_count % 2 == 0:
                c.setFillColorRGB(0.95, 0.95, 0.95)
                c.rect(0.75*inch, y_position - 0.05*inch, width - 1.5*inch, 0.25*inch, fill=True, stroke=False)
            
            c.setFillColorRGB(0, 0, 0)
            c.drawString(1*inch, y_position, item['name'][:30])
            c.drawString(3.65*inch, y_position, str(item['quantity']))
            c.drawString(4.5*inch, y_position, f"UGX {item['price']:,.0f}")
            c.drawString(5.7*inch, y_position, f"UGX {item['subtotal']:,.0f}")
            y_position -= 0.25*inch
        
        # Total Section
        y_position -= 0.3*inch
        c.setLineWidth(1)
        c.setStrokeColorRGB(0, 0, 0)
        c.line(4.5*inch, y_position, 7*inch, y_position)
        
        y_position -= 0.3*inch
        c.setFont("Helvetica-Bold", 14)
        c.drawString(4.5*inch, y_position, "TOTAL:")
        c.setFillColorRGB(0.15, 0.68, 0.38)  # Green
        c.drawString(5.7*inch, y_position, f"UGX {total:,.0f}")
        
        # Footer
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Italic", 9)
        c.drawString(1*inch, 1.2*inch, "Thank you for shopping with us!")
        c.setFont("Helvetica", 8)
        c.drawString(1*inch, 1*inch, "For inquiries: contact@jksboutique.com | +256-XXX-XXXXXX")
        c.drawString(1*inch, 0.8*inch, "This is a computer-generated invoice.")
        
        c.save()
        return full_path
    
    @staticmethod
    def open_receipt(file_path):
        """Open the receipt PDF with the default PDF viewer"""
        try:
            if sys.platform == 'win32':
                os.startfile(file_path)
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{file_path}"')
            else:  # Linux
                os.system(f'xdg-open "{file_path}"')
            return True
        except Exception as e:
            print(f"Error opening file: {e}")
            return False


class RegistrationPage(tk.Frame):
    """Registration page for new users - with scrolling support"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#2c3e50')
        self.controller = controller
        
        # Create main container with Canvas for scrolling
        main_container = tk.Frame(self, bg='#ecf0f1', bd=2, relief='raised')
        main_container.place(relx=0.5, rely=0.5, anchor='center', width=480, height=600)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_container, bg='#ecf0f1', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Title
        title = tk.Label(scrollable_frame, text="JK's Boutique & Kid's Wear", 
                        font=('Arial', 18, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=(20, 10))
        
        subtitle = tk.Label(scrollable_frame, text="Create New Account", 
                           font=('Arial', 14), bg='#ecf0f1', fg='#34495e')
        subtitle.pack(pady=(0, 20))
        
        # Full Name
        tk.Label(scrollable_frame, text="Full Name:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(pady=(10, 5))
        self.fullname_entry = tk.Entry(scrollable_frame, font=('Arial', 11), width=35)
        self.fullname_entry.pack(pady=5)
        
        # Email
        tk.Label(scrollable_frame, text="Email:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(pady=(15, 5))
        self.email_entry = tk.Entry(scrollable_frame, font=('Arial', 11), width=35)
        self.email_entry.pack(pady=5)
        
        # Username
        tk.Label(scrollable_frame, text="Username:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(pady=(15, 5))
        self.username_entry = tk.Entry(scrollable_frame, font=('Arial', 11), width=35)
        self.username_entry.pack(pady=5)
        
        # Password
        tk.Label(scrollable_frame, text="Password:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(pady=(15, 5))
        self.password_entry = tk.Entry(scrollable_frame, font=('Arial', 11), width=35, show='*')
        self.password_entry.pack(pady=5)
        
        # Confirm Password
        tk.Label(scrollable_frame, text="Confirm Password:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(pady=(15, 5))
        self.confirm_password_entry = tk.Entry(scrollable_frame, font=('Arial', 11), width=35, show='*')
        self.confirm_password_entry.pack(pady=5)
        
        # Register button
        register_btn = tk.Button(scrollable_frame, text="Register", font=('Arial', 12, 'bold'),
                                bg='#27ae60', fg='white', width=18, height=2,
                                command=self.register)
        register_btn.pack(pady=20)
        
        # Back to Login button
        back_btn = tk.Button(scrollable_frame, text="← Back to Login", font=('Arial', 10),
                            bg='#95a5a6', fg='white', width=18,
                            command=lambda: controller.show_frame("LoginPage"))
        back_btn.pack(pady=(5, 20))
        
        # Bind Enter key
        self.confirm_password_entry.bind('<Return>', lambda e: self.register())
    
    def register(self):
        full_name = self.fullname_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validation
        if not full_name or not email or not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters!")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        if '@' not in email or '.' not in email:
            messagebox.showerror("Error", "Please enter a valid email address!")
            return
          # Check if username already exists
        if self.controller.data_manager.username_exists(username):
            messagebox.showerror("Error", "Username already exists! Please choose another.")
            return
        
        # Register user
        user = User(username, password, full_name, email)
        success = self.controller.data_manager.register_user(user)
        
        if not success:
            messagebox.showerror("Error", "Failed to register user. Please try again.")
            return
        
        messagebox.showinfo("Success", f"Account created successfully!\nWelcome, {full_name}!")
        
        # Clear fields
        self.fullname_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)
        
        # Go to login page
        self.controller.show_frame("LoginPage")


class LoginPage(tk.Frame):
    """Login page for owner authentication"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#2c3e50')
        self.controller = controller
          # Create main container
        container = tk.Frame(self, bg='#ecf0f1', bd=2, relief='raised')
        container.place(relx=0.5, rely=0.5, anchor='center', width=400, height=450)
        
        # Title
        title = tk.Label(container, text="JK's Boutique & Kid's Wear", 
                        font=('Arial', 18, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=20)
        
        subtitle = tk.Label(container, text="Owner Login", 
                           font=('Arial', 14), bg='#ecf0f1', fg='#34495e')
        subtitle.pack(pady=10)
        
        # Username
        tk.Label(container, text="Username:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(pady=(20, 5))
        self.username_entry = tk.Entry(container, font=('Arial', 11), width=30)
        self.username_entry.pack(pady=5)
          # Password
        tk.Label(container, text="Password:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(pady=(10, 5))
        self.password_entry = tk.Entry(container, font=('Arial', 11), width=30, show='*')
        self.password_entry.pack(pady=5)
          # Login button
        login_btn = tk.Button(container, text="Login", font=('Arial', 12, 'bold'),
                             bg='#27ae60', fg='white', width=15, height=2,
                             command=self.login)
        login_btn.pack(pady=15)
        
        # Separator
        tk.Label(container, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 
                font=('Arial', 8), bg='#ecf0f1', fg='#bdc3c7').pack(pady=5)
        
        # Register section - MORE VISIBLE
        tk.Label(container, text="Don't have an account?", 
                font=('Arial', 11, 'bold'), bg='#ecf0f1', fg='#34495e').pack(pady=(5, 5))
        
        register_btn = tk.Button(container, text="📝 REGISTER HERE", 
                                font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                                width=20, height=2, cursor='hand2',
                                command=lambda: self.controller.show_frame("RegistrationPage"))
        register_btn.pack(pady=5)
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Check default owner account
        if username == "owner" and password == "admin123":
            self.controller.show_frame("DashboardPage")
            return
        
        # Check registered users
        user = self.controller.data_manager.get_user(username)
        if user and user.password == password:
            self.controller.show_frame("DashboardPage")
        else:
            messagebox.showerror("Error", "Invalid username or password!")


class DashboardPage(tk.Frame):
    """Dashboard page showing business overview"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#ecf0f1')
        self.controller = controller
        
        # Header
        header = tk.Frame(self, bg='#2c3e50', height=80)
        header.pack(fill='x')
        
        tk.Label(header, text="Dashboard", font=('Arial', 24, 'bold'),
                bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=20)
        
        logout_btn = tk.Button(header, text="Logout", font=('Arial', 10),
                              bg='#e74c3c', fg='white', command=self.logout)
        logout_btn.pack(side='right', padx=20)
        
        # Main content
        content = tk.Frame(self, bg='#ecf0f1')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Statistics cards
        stats_frame = tk.Frame(content, bg='#ecf0f1')
        stats_frame.pack(fill='x', pady=20)
        
        self.total_products_label = self.create_stat_card(stats_frame, "Total Products", "0", '#3498db')
        self.total_products_label.pack(side='left', padx=10)
        
        self.total_value_label = self.create_stat_card(stats_frame, "Total Inventory Value", "UGX 0", '#2ecc71')
        self.total_value_label.pack(side='left', padx=10)
        
        self.low_stock_label = self.create_stat_card(stats_frame, "Low Stock Items", "0", '#e74c3c')
        self.low_stock_label.pack(side='left', padx=10)
          # Navigation buttons
        nav_frame = tk.Frame(content, bg='#ecf0f1')
        nav_frame.pack(expand=True)
        
        buttons = [
            ("Add New Stock", "AddStockPage", '#27ae60'),
            ("View Inventory", "InventoryPage", '#3498db'),
            ("Generate Receipt", "ReceiptPage", '#f39c12')
        ]
        
        for text, page, color in buttons:
            btn = tk.Button(nav_frame, text=text, font=('Arial', 14, 'bold'),
                           bg=color, fg='white', width=20, height=3,
                           command=lambda p=page: self.controller.show_frame(p))
            btn.pack(pady=15)
    
    def create_stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg='white', bd=2, relief='raised', width=200, height=120)
        card.pack_propagate(False)
        
        tk.Label(card, text=title, font=('Arial', 11), bg='white', fg='#7f8c8d').pack(pady=(15, 5))
        value_label = tk.Label(card, text=value, font=('Arial', 20, 'bold'), bg='white', fg=color)
        value_label.pack()
        
        return value_label
    
    def update_stats(self):
        db = self.controller.data_manager.db
        
        total_products = len(db.get_all_products())
        total_value = db.get_total_inventory_value()
        low_stock = db.get_low_stock_count()
        
        self.total_products_label.config(text=str(total_products))
        self.total_value_label.config(text=f"UGX {total_value:,.0f}")
        self.low_stock_label.config(text=str(low_stock))
    
    def logout(self):
        self.controller.show_frame("LoginPage")


class AddStockPage(tk.Frame):
    """Page for adding new stock"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#ecf0f1')
        self.controller = controller
        
        # Header
        header = tk.Frame(self, bg='#2c3e50', height=80)
        header.pack(fill='x')
        
        tk.Label(header, text="Add New Stock", font=('Arial', 24, 'bold'),
                bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=20)
        
        back_btn = tk.Button(header, text="← Back to Dashboard", font=('Arial', 10),
                            bg='#34495e', fg='white', 
                            command=lambda: controller.show_frame("DashboardPage"))
        back_btn.pack(side='right', padx=20)
        
        # Form
        form_frame = tk.Frame(self, bg='white', bd=2, relief='raised')
        form_frame.place(relx=0.5, rely=0.5, anchor='center', width=500, height=400)
        
        tk.Label(form_frame, text="Product Details", font=('Arial', 16, 'bold'),
                bg='white', fg='#2c3e50').pack(pady=20)
        
        # Product Name
        tk.Label(form_frame, text="Product Name:", font=('Arial', 11),
                bg='white', fg='#2c3e50').pack(pady=(10, 5))
        self.name_entry = tk.Entry(form_frame, font=('Arial', 11), width=40)
        self.name_entry.pack(pady=5)
        
        # Price
        tk.Label(form_frame, text="Price (UGX):", font=('Arial', 11),
                bg='white', fg='#2c3e50').pack(pady=(10, 5))
        self.price_entry = tk.Entry(form_frame, font=('Arial', 11), width=40)
        self.price_entry.pack(pady=5)
        
        # Quantity
        tk.Label(form_frame, text="Quantity:", font=('Arial', 11),
                bg='white', fg='#2c3e50').pack(pady=(10, 5))
        self.quantity_entry = tk.Entry(form_frame, font=('Arial', 11), width=40)
        self.quantity_entry.pack(pady=5)
        
        # Add button
        add_btn = tk.Button(form_frame, text="Add Product", font=('Arial', 12, 'bold'),
                           bg='#27ae60', fg='white', width=20, height=2,
                           command=self.add_product)
        add_btn.pack(pady=20)
    
    def add_product(self):
        name = self.name_entry.get().strip()
        price_str = self.price_entry.get().strip()
        quantity_str = self.quantity_entry.get().strip()
        
        if not name or not price_str or not quantity_str:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            price = float(price_str)
            quantity = int(quantity_str)
            
            if price <= 0 or quantity <= 0:
                messagebox.showerror("Error", "Price and quantity must be positive!")
                return
            
            product_id = self.controller.data_manager.get_next_id()
            product = Product(product_id, name, price, quantity)
            self.controller.data_manager.add_product(product)
            
            messagebox.showinfo("Success", f"Product '{name}' added successfully!")
            
            # Clear fields
            self.name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid price or quantity format!")


class InventoryPage(tk.Frame):
    """Page for viewing and managing inventory"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#ecf0f1')
        self.controller = controller
        
        # Header
        header = tk.Frame(self, bg='#2c3e50', height=80)
        header.pack(fill='x')
        
        tk.Label(header, text="Inventory Management", font=('Arial', 24, 'bold'),
                bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=20)
        
        back_btn = tk.Button(header, text="← Back to Dashboard", font=('Arial', 10),
                            bg='#34495e', fg='white',
                            command=lambda: controller.show_frame("DashboardPage"))
        back_btn.pack(side='right', padx=20)
        
        # Content
        content = tk.Frame(self, bg='#ecf0f1')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Treeview
        tree_frame = tk.Frame(content, bg='white', bd=2, relief='raised')
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        y_scroll = tk.Scrollbar(tree_frame)
        y_scroll.pack(side='right', fill='y')
        
        x_scroll = tk.Scrollbar(tree_frame, orient='horizontal')
        x_scroll.pack(side='bottom', fill='x')
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Price', 'Quantity', 'Total Value'),
                                show='headings', yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        y_scroll.config(command=self.tree.yview)
        x_scroll.config(command=self.tree.xview)
        
        # Define columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Product Name')
        self.tree.heading('Price', text='Price (UGX)')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Total Value', text='Total Value (UGX)')
        
        self.tree.column('ID', width=50)
        self.tree.column('Name', width=250)
        self.tree.column('Price', width=120)
        self.tree.column('Quantity', width=100)
        self.tree.column('Total Value', width=150)
        
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(content, bg='#ecf0f1')
        btn_frame.pack(fill='x', pady=10)
        
        refresh_btn = tk.Button(btn_frame, text="Refresh", font=('Arial', 11),
                               bg='#3498db', fg='white', width=12,
                               command=self.load_inventory)
        refresh_btn.pack(side='left', padx=5)
        
        delete_btn = tk.Button(btn_frame, text="Delete Selected", font=('Arial', 11),
                              bg='#e74c3c', fg='white', width=12,
                              command=self.delete_product)
        delete_btn.pack(side='left', padx=5)
    
    def load_inventory(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load products
        products = self.controller.data_manager.get_all_products()
        for product in products:
            total_value = product.price * product.quantity
            self.tree.insert('', 'end', values=(
                product.product_id,
                product.name,
                f"{product.price:,.0f}",
                product.quantity,
                f"{total_value:,.0f}"
            ))
    
    def delete_product(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product to delete!")
            return
        
        item = self.tree.item(selection[0])
        product_id = int(item['values'][0])
        product_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{product_name}'?"):
            self.controller.data_manager.delete_product(product_id)
            self.load_inventory()
            messagebox.showinfo("Success", "Product deleted successfully!")


class ReceiptPage(tk.Frame):
    """Page for generating receipts"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#ecf0f1')
        self.controller = controller
        self.cart_items = []
        
        # Header
        header = tk.Frame(self, bg='#2c3e50', height=80)
        header.pack(fill='x')
        
        tk.Label(header, text="Generate Receipt", font=('Arial', 24, 'bold'),
                bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=20)
        
        back_btn = tk.Button(header, text="← Back to Dashboard", font=('Arial', 10),
                            bg='#34495e', fg='white',
                            command=lambda: controller.show_frame("DashboardPage"))
        back_btn.pack(side='right', padx=20)
        
        # Main content
        content = tk.Frame(self, bg='#ecf0f1')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left side - Product selection
        left_frame = tk.Frame(content, bg='white', bd=2, relief='raised')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(left_frame, text="Select Product", font=('Arial', 14, 'bold'),
                bg='white').pack(pady=10)
        
        tk.Label(left_frame, text="Product:", font=('Arial', 11), bg='white').pack(pady=(10, 5))
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(left_frame, textvariable=self.product_var,
                                         font=('Arial', 11), width=30, state='readonly')
        self.product_combo.pack(pady=5)
        
        tk.Label(left_frame, text="Quantity:", font=('Arial', 11), bg='white').pack(pady=(10, 5))
        self.qty_entry = tk.Entry(left_frame, font=('Arial', 11), width=32)
        self.qty_entry.pack(pady=5)
        
        add_to_cart_btn = tk.Button(left_frame, text="Add to Cart", font=('Arial', 12, 'bold'),
                                    bg='#27ae60', fg='white', width=20,
                                    command=self.add_to_cart)
        add_to_cart_btn.pack(pady=20)
        
        # Right side - Cart
        right_frame = tk.Frame(content, bg='white', bd=2, relief='raised')
        right_frame.pack(side='right', fill='both', expand=True)
        
        tk.Label(right_frame, text="Cart", font=('Arial', 14, 'bold'),
                bg='white').pack(pady=10)
        
        # Cart listbox
        cart_frame = tk.Frame(right_frame, bg='white')
        cart_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        cart_scroll = tk.Scrollbar(cart_frame)
        cart_scroll.pack(side='right', fill='y')
        
        self.cart_listbox = tk.Listbox(cart_frame, font=('Arial', 10),
                                       yscrollcommand=cart_scroll.set, height=10)
        self.cart_listbox.pack(side='left', fill='both', expand=True)
        cart_scroll.config(command=self.cart_listbox.yview)
        
        # Total
        self.total_label = tk.Label(right_frame, text="Total: UGX 0",
                                    font=('Arial', 16, 'bold'), bg='white', fg='#27ae60')
        self.total_label.pack(pady=10)
          # Buttons
        btn_frame = tk.Frame(right_frame, bg='white')
        btn_frame.pack(pady=10)
        
        clear_btn = tk.Button(btn_frame, text="🗑️ Clear Cart", font=('Arial', 11, 'bold'),
                             bg='#e74c3c', fg='white', width=14, height=2,
                             command=self.clear_cart)
        clear_btn.pack(side='left', padx=5)
        
        generate_btn = tk.Button(btn_frame, text="📄 Generate Receipt", font=('Arial', 11, 'bold'),
                                bg='#27ae60', fg='white', width=18, height=2,
                                command=self.generate_receipt)
        generate_btn.pack(side='left', padx=5)
        
        # Status label
        self.status_label = tk.Label(right_frame, text="Add items to cart and click Generate Receipt", 
                                    font=('Arial', 9, 'italic'), bg='white', fg='#7f8c8d')
        self.status_label.pack(pady=5)
    
    def load_products(self):
        products = self.controller.data_manager.get_all_products()
        product_names = [f"{p.name} (ID: {p.product_id}, Stock: {p.quantity})" for p in products]
        self.product_combo['values'] = product_names
    
    def add_to_cart(self):
        selection = self.product_var.get()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product!")
            return
        
        try:            # Extract product ID from selection
            product_id = int(selection.split("ID: ")[1].split(",")[0])
            quantity = int(self.qty_entry.get())
            
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be positive!")
                return
            
            product = self.controller.data_manager.get_product(product_id)
            if not product:
                messagebox.showerror("Error", "Product not found!")
                return
            
            if quantity > product.quantity:
                messagebox.showerror("Error", f"Only {product.quantity} items available in stock!")
                return
            
            # Add to cart
            item = {
                'product_id': product_id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'subtotal': product.price * quantity
            }
            self.cart_items.append(item)
              # Update display
            self.cart_listbox.insert(tk.END, 
                f"{item['name']} x{quantity} - UGX {item['subtotal']:,.0f}")
            
            self.update_total()
            self.qty_entry.delete(0, tk.END)
            messagebox.showinfo("Added", f"{product.name} added to cart!")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid quantity: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add to cart: {str(e)}")
    
    def clear_cart(self):
        self.cart_items = []
        self.cart_listbox.delete(0, tk.END)
        self.update_total()
    
    def update_total(self):
        total = sum(item['subtotal'] for item in self.cart_items)
        self.total_label.config(text=f"Total: UGX {total:,.0f}")
    
    def generate_receipt(self):
        """Generate PDF invoice for items in cart"""
        print("DEBUG: generate_receipt called")  # Debug
        print(f"DEBUG: Cart items count: {len(self.cart_items)}")  # Debug
        
        if not self.cart_items:
            messagebox.showwarning("Warning", "Cart is empty! Please add items first.")
            return
        
        try:
            print("DEBUG: Getting database manager")  # Debug
            db = self.controller.data_manager.db
            receipt_number = db.get_next_receipt_number()
            print(f"DEBUG: Receipt number: {receipt_number}")  # Debug
            
            total = sum(item['subtotal'] for item in self.cart_items)
            print(f"DEBUG: Total: {total}")  # Debug
            
            print("DEBUG: Calling ReceiptGenerator.generate_receipt")  # Debug
            full_path = ReceiptGenerator.generate_receipt(self.cart_items, total, receipt_number)
            print(f"DEBUG: Invoice saved to: {full_path}")  # Debug
            
            # Save receipt to database
            print("DEBUG: Saving to database")  # Debug
            db.save_receipt(receipt_number, total, os.path.basename(full_path), self.cart_items)
            
            # Update inventory
            print("DEBUG: Updating inventory")  # Debug
            for item in self.cart_items:
                product = self.controller.data_manager.get_product(item['product_id'])
                if product:
                    new_quantity = product.quantity - item['quantity']
                    self.controller.data_manager.update_product(
                        product.product_id, product.name, product.price, new_quantity
                    )
            
            # Get receipts folder for display
            receipts_folder = ReceiptGenerator.get_receipts_folder()
            print("DEBUG: Showing success message")  # Debug
            
            # Ask if user wants to open the invoice
            result = messagebox.askyesno("Invoice Generated!", 
                              f"✅ Invoice generated successfully!\n\n"
                              f"Invoice #: {receipt_number:05d}\n"
                              f"Total: UGX {total:,.0f}\n\n"
                              f"Saved to:\n{receipts_folder}\n\n"
                              f"File: {os.path.basename(full_path)}\n\n"
                              f"📥 Would you like to open the invoice now?")
            
            if result:
                # Open the invoice
                if ReceiptGenerator.open_receipt(full_path):
                    print("DEBUG: Invoice opened successfully")
                else:
                    messagebox.showinfo("Info", f"Please open the invoice manually from:\n{full_path}")
            
            print("DEBUG: Clearing cart")  # Debug
            self.clear_cart()
            self.status_label.config(text="✅ Invoice generated successfully!", fg='#27ae60')
            print("DEBUG: Invoice generation complete!")  # Debug
            
        except Exception as e:
            print(f"DEBUG ERROR: {str(e)}")  # Debug
            import traceback
            traceback.print_exc()
            self.status_label.config(text="❌ Failed to generate invoice", fg='#e74c3c')
            messagebox.showerror("Error", f"Failed to generate invoice!\n\nError: {str(e)}\n\nPlease check that:\n1. Cart has items\n2. Products exist in database\n3. Write permissions available")


class BoutiqueApp(tk.Tk):
    """Main application class"""
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title("JK's Boutique and Kid's Wear")
        self.geometry("900x650")
        self.resizable(True, True)
        
        # Initialize data manager
        self.data_manager = DataManager()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Container for frames
        container = tk.Frame(self)
        container.pack(fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)        # Dictionary to hold frames
        self.frames = {}
        
        # Create all frames
        for F in (LoginPage, RegistrationPage, DashboardPage, AddStockPage, InventoryPage, ReceiptPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        
        # Show login page first
        self.show_frame("LoginPage")
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Reports menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Receipt History", command=self.show_receipt_history)
        reports_menu.add_command(label="Low Stock Report", command=self.show_low_stock_report)
        reports_menu.add_command(label="Inventory Report", command=self.show_inventory_report)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def open_db_browser(self):
        """Open database browser window"""
        browser_window = tk.Toplevel(self)
        browser_window.title("Database Browser - JK's Boutique")
        browser_window.geometry("1000x600")
        
        # Header
        header = tk.Frame(browser_window, bg='#2c3e50', height=60)
        header.pack(fill='x')
        tk.Label(header, text="🗄️ SQLite Database Browser", font=('Arial', 18, 'bold'),
                bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=15)
        
        db_path = os.path.abspath(self.data_manager.db.db_name)
        tk.Label(header, text=f"Database: {db_path}", font=('Arial', 9),
                bg='#2c3e50', fg='#ecf0f1').pack(side='right', padx=20)
        
        # Main container
        main_frame = tk.Frame(browser_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left side - Table list
        left_frame = tk.Frame(main_frame, bg='#ecf0f1', width=200)
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        left_frame.pack_propagate(False)
        
        tk.Label(left_frame, text="Tables", font=('Arial', 12, 'bold'),
                bg='#ecf0f1').pack(pady=10)
        
        table_listbox = tk.Listbox(left_frame, font=('Arial', 10))
        table_listbox.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        tables = ['products', 'users', 'receipts', 'receipt_items']
        for table in tables:
            table_listbox.insert(tk.END, table)
        
        # Right side - Table data
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Control buttons
        control_frame = tk.Frame(right_frame)
        control_frame.pack(fill='x', pady=(0, 5))
        
        tk.Label(control_frame, text="Selected Table:", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        table_name_label = tk.Label(control_frame, text="None", font=('Arial', 10),
                                    fg='#3498db')
        table_name_label.pack(side='left', padx=5)
        
        refresh_btn = tk.Button(control_frame, text="🔄 Refresh", font=('Arial', 9),
                               bg='#3498db', fg='white',
                               command=lambda: load_table_data())
        refresh_btn.pack(side='right', padx=5)
        
        # Treeview for table data
        tree_frame = tk.Frame(right_frame)
        tree_frame.pack(fill='both', expand=True)
        
        y_scroll = tk.Scrollbar(tree_frame)
        y_scroll.pack(side='right', fill='y')
        
        x_scroll = tk.Scrollbar(tree_frame, orient='horizontal')
        x_scroll.pack(side='bottom', fill='x')
        
        tree = ttk.Treeview(tree_frame, yscrollcommand=y_scroll.set, 
                           xscrollcommand=x_scroll.set)
        y_scroll.config(command=tree.yview)
        x_scroll.config(command=tree.xview)
        tree.pack(fill='both', expand=True)
        
        # Info label
        info_label = tk.Label(right_frame, text="Select a table to view data", 
                            font=('Arial', 9), fg='#7f8c8d')
        info_label.pack(pady=5)
        
        def load_table_data():
            selection = table_listbox.curselection()
            if not selection:
                return
            
            table_name = table_listbox.get(selection[0])
            table_name_label.config(text=table_name)
            
            # Clear existing tree
            tree.delete(*tree.get_children())
            for col in tree["columns"]:
                tree.heading(col, text="")
            tree["columns"] = ()
            tree["show"] = "tree headings"
            
            try:
                db = self.data_manager.db
                # Get column names
                db.cursor.execute(f"PRAGMA table_info({table_name})")
                columns_info = db.cursor.fetchall()
                column_names = [col[1] for col in columns_info]
                
                # Configure tree columns
                tree["columns"] = column_names
                tree["show"] = "headings"
                
                for col in column_names:
                    tree.heading(col, text=col)
                    tree.column(col, width=150)
                
                # Get data
                db.cursor.execute(f"SELECT * FROM {table_name}")
                rows = db.cursor.fetchall()
                
                for row in rows:
                    tree.insert('', 'end', values=row)
                
                info_label.config(text=f"Showing {len(rows)} records from '{table_name}' table")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load table data: {str(e)}")
        
        # Bind table selection
        table_listbox.bind('<<ListboxSelect>>', lambda e: load_table_data())
        
        # SQL Query section
        query_frame = tk.Frame(browser_window, bg='#f8f9fa')
        query_frame.pack(fill='x', padx=10, pady=(5, 10))
        
        tk.Label(query_frame, text="SQL Query:", font=('Arial', 10, 'bold'),
                bg='#f8f9fa').pack(anchor='w', padx=5, pady=(5, 2))
        
        query_text = tk.Text(query_frame, height=3, font=('Courier', 9))
        query_text.pack(fill='x', padx=5, pady=(0, 5))
        query_text.insert('1.0', 'SELECT * FROM products LIMIT 10;')
        
        def execute_query():
            query = query_text.get('1.0', tk.END).strip()
            if not query:
                return
            
            try:
                db = self.data_manager.db
                db.cursor.execute(query)
                
                if query.strip().upper().startswith('SELECT'):
                    # Clear and show results
                    tree.delete(*tree.get_children())
                    
                    # Get column names from cursor
                    if db.cursor.description:
                        column_names = [desc[0] for desc in db.cursor.description]
                        tree["columns"] = column_names
                        tree["show"] = "headings"
                        
                        for col in column_names:
                            tree.heading(col, text=col)
                            tree.column(col, width=150)
                        
                        rows = db.cursor.fetchall()
                        for row in rows:
                            tree.insert('', 'end', values=row)
                        
                        info_label.config(text=f"Query returned {len(rows)} records")
                        table_name_label.config(text="Custom Query")
                else:
                    db.conn.commit()
                    messagebox.showinfo("Success", "Query executed successfully!")
                    load_table_data()
                    
            except Exception as e:
                messagebox.showerror("Query Error", f"Failed to execute query:\n{str(e)}")
        
        query_btn = tk.Button(query_frame, text="▶ Execute Query", font=('Arial', 9, 'bold'),
                             bg='#27ae60', fg='white', command=execute_query)
        query_btn.pack(pady=(0, 5))
        
        # Select first table by default
        table_listbox.selection_set(0)
        load_table_data()
    
    def export_to_json(self):
        """Export database to JSON files"""
        try:
            # Export products
            products = self.data_manager.get_all_products()
            products_data = [p.to_dict() for p in products]
            with open('products_export.json', 'w') as f:
                json.dump(products_data, f, indent=4)
            
            # Export users
            db = self.data_manager.db
            db.cursor.execute('SELECT username, full_name, email FROM users')
            users = db.cursor.fetchall()
            users_data = [{'username': u[0], 'full_name': u[1], 'email': u[2]} for u in users]
            with open('users_export.json', 'w') as f:
                json.dump(users_data, f, indent=4)
            
            messagebox.showinfo("Export Successful", 
                              "Data exported successfully!\n\n"
                              "Files created:\n"
                              "- products_export.json\n"
                              "- users_export.json")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export data: {str(e)}")
    
    def backup_database(self):
        """Create a backup of the database"""
        try:
            import shutil
            db_path = self.data_manager.db.db_name
            backup_name = f"boutique_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2(db_path, backup_name)
            messagebox.showinfo("Backup Successful", f"Database backed up successfully!\n\nBackup file: {backup_name}")
        except Exception as e:
            messagebox.showerror("Backup Failed", f"Failed to backup database: {str(e)}")
    
    def show_db_info(self):
        """Show database information"""
        try:
            db = self.data_manager.db
            db_path = os.path.abspath(db.db_name)
            db_size = os.path.getsize(db_path) / 1024  # Size in KB
            
            # Get table counts
            db.cursor.execute('SELECT COUNT(*) FROM products')
            product_count = db.cursor.fetchone()[0]
            
            db.cursor.execute('SELECT COUNT(*) FROM users')
            user_count = db.cursor.fetchone()[0]
            
            db.cursor.execute('SELECT COUNT(*) FROM receipts')
            receipt_count = db.cursor.fetchone()[0]
            
            info = (
                f"Database Information\n"
                f"{'='*40}\n\n"
                f"Database File: {db_path}\n"
                f"Database Size: {db_size:.2f} KB\n\n"
                f"Tables:\n"
                f"  • Products: {product_count} records\n"
                f"  • Users: {user_count} records\n"                f"  • Receipts: {receipt_count} records\n\n"
                f"Database Type: SQLite 3"
            )
            
            messagebox.showinfo("Database Information", info)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get database info: {str(e)}")
    
    def show_receipt_history(self):
        """Show receipt history window with download/open functionality"""
        history_window = tk.Toplevel(self)
        history_window.title("Invoice History - Download Invoices")
        history_window.geometry("800x550")
        
        # Header
        header = tk.Frame(history_window, bg='#2c3e50', height=60)
        header.pack(fill='x')
        tk.Label(header, text="📄 Invoice History", font=('Arial', 18, 'bold'),
                bg='#2c3e50', fg='white').pack(pady=15)
        
        # Treeview
        tree_frame = tk.Frame(history_window)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        tree = ttk.Treeview(tree_frame, columns=('Receipt#', 'Total', 'Date', 'Filename'),
                           show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading('Receipt#', text='Invoice #')
        tree.heading('Total', text='Total Amount')
        tree.heading('Date', text='Date')
        tree.heading('Filename', text='Filename')
        
        tree.column('Receipt#', width=100)
        tree.column('Total', width=150)
        tree.column('Date', width=180)
        tree.column('Filename', width=350)
        
        tree.pack(fill='both', expand=True)
        
        # Load data
        receipts = self.data_manager.db.get_receipt_history()
        receipt_map = {}  # Map tree items to filenames
        
        for receipt in receipts:
            item_id = tree.insert('', 'end', values=(
                f"{receipt[1]:05d}",  # receipt_number formatted
                f"UGX {receipt[2]:,.0f}",  # total_amount
                receipt[4],  # created_at
                receipt[3]   # filename
            ))
            receipt_map[item_id] = receipt[3]  # Store filename
        
        # Button frame
        btn_frame = tk.Frame(history_window, bg='#ecf0f1')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        def open_selected_invoice():
            """Open the selected invoice PDF"""
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select an invoice to open")
                return
            
            filename = receipt_map[selection[0]]
            receipts_folder = ReceiptGenerator.get_receipts_folder()
            full_path = os.path.join(receipts_folder, filename)
            
            if not os.path.exists(full_path):
                messagebox.showerror("File Not Found", 
                                   f"Invoice file not found:\n{full_path}\n\n"
                                   f"The file may have been moved or deleted.")
                return
            
            if ReceiptGenerator.open_receipt(full_path):
                messagebox.showinfo("Success", "Invoice opened successfully!")
            else:
                messagebox.showerror("Error", f"Could not open invoice.\n\nPath: {full_path}")
        
        def open_receipts_folder():
            """Open the receipts folder in file explorer"""
            receipts_folder = ReceiptGenerator.get_receipts_folder()
            try:
                if sys.platform == 'win32':
                    os.startfile(receipts_folder)
                elif sys.platform == 'darwin':
                    os.system(f'open "{receipts_folder}"')
                else:
                    os.system(f'xdg-open "{receipts_folder}"')
            except Exception as e:
                messagebox.showerror("Error", f"Could not open folder:\n{str(e)}")
        
        # Buttons
        open_btn = tk.Button(btn_frame, text="📥 Open Selected Invoice", font=('Arial', 11, 'bold'),
                           bg='#27ae60', fg='white', width=22, height=2,
                           command=open_selected_invoice)
        open_btn.pack(side='left', padx=5)
        
        folder_btn = tk.Button(btn_frame, text="📁 Open Invoices Folder", font=('Arial', 11, 'bold'),
                             bg='#3498db', fg='white', width=22, height=2,
                             command=open_receipts_folder)
        folder_btn.pack(side='left', padx=5)
        
        close_btn = tk.Button(btn_frame, text="Close", font=('Arial', 11),
                            bg='#95a5a6', fg='white', width=12, height=2,
                            command=history_window.destroy)
        close_btn.pack(side='right', padx=5)
        
        # Instructions
        info_label = tk.Label(history_window, 
                            text="💡 Tip: Double-click an invoice to open it, or select and click 'Open Selected Invoice'",
                            font=('Arial', 9, 'italic'), bg='#ecf0f1', fg='#7f8c8d')
        info_label.pack(pady=5)
        
        # Double-click to open
        tree.bind('<Double-1>', lambda e: open_selected_invoice())
    
    def show_low_stock_report(self):
        """Show low stock items report"""
        report_window = tk.Toplevel(self)
        report_window.title("Low Stock Report")
        report_window.geometry("600x400")
        
        # Header
        header = tk.Frame(report_window, bg='#e74c3c', height=60)
        header.pack(fill='x')
        tk.Label(header, text="⚠️ Low Stock Items (< 10 units)", font=('Arial', 16, 'bold'),
                bg='#e74c3c', fg='white').pack(pady=15)
        
        # Treeview
        tree_frame = tk.Frame(report_window)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Quantity', 'Price'),
                           show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Product Name')
        tree.heading('Quantity', text='Quantity')
        tree.heading('Price', text='Price')
        
        tree.pack(fill='both', expand=True)
        
        # Load low stock items
        products = self.data_manager.get_all_products()
        low_stock_items = [p for p in products if p.quantity < 10]
        
        for product in low_stock_items:
            tree.insert('', 'end', values=(
                product.product_id,
                product.name,
                product.quantity,
                f"UGX {product.price:,.0f}"
            ))
        
        if not low_stock_items:
            tk.Label(report_window, text="✓ All items have sufficient stock!", 
                    font=('Arial', 14), fg='#27ae60').pack(pady=20)
    
    def show_inventory_report(self):
        """Show full inventory report"""
        report_window = tk.Toplevel(self)
        report_window.title("Inventory Report")
        report_window.geometry("800x600")
        
        # Header
        header = tk.Frame(report_window, bg='#3498db', height=60)
        header.pack(fill='x')
        tk.Label(header, text="📊 Complete Inventory Report", font=('Arial', 16, 'bold'),
                bg='#3498db', fg='white').pack(pady=15)
        
        # Summary
        summary_frame = tk.Frame(report_window, bg='#ecf0f1')
        summary_frame.pack(fill='x', padx=10, pady=10)
        
        db = self.data_manager.db
        total_products = len(db.get_all_products())
        total_value = db.get_total_inventory_value()
        
        tk.Label(summary_frame, text=f"Total Products: {total_products}", 
                font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(side='left', padx=20)
        tk.Label(summary_frame, text=f"Total Value: UGX {total_value:,.0f}", 
                font=('Arial', 12, 'bold'), bg='#ecf0f1', fg='#27ae60').pack(side='left', padx=20)
        
        # Treeview
        tree_frame = tk.Frame(report_window)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Price', 'Quantity', 'Total'),
                           show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Product Name')
        tree.heading('Price', text='Price (UGX)')
        tree.heading('Quantity', text='Quantity')
        tree.heading('Total', text='Total Value (UGX)')
        
        tree.pack(fill='both', expand=True)
        
        # Load data
        products = self.data_manager.get_all_products()
        for product in products:
            total_value = product.price * product.quantity
            tree.insert('', 'end', values=(
                product.product_id,
                product.name,
                f"{product.price:,.0f}",
                product.quantity,
                f"{total_value:,.0f}"
            ))
    
    def show_about(self):
        """Show about dialog"""
        about_text = (
            "JK's Boutique and Kid's Wear\n"
            "Inventory Management System\n\n"
            "Version 2.0 - SQLite Edition\n\n"
            "Features:\n"
            "• User Registration & Authentication\n"
            "• Product Management\n"
            "• Receipt Generation (PDF)\n"
            "• SQLite Database Integration\n"
            "• Inventory Tracking\n"
            "• Reports & Analytics\n\n"
            "Author: Kiwumulo Joanah\n"
            "© 2025 JK's Boutique"
        )
        messagebox.showinfo("About", about_text)
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
        # Update specific frames when shown
        if page_name == "DashboardPage":
            frame.update_stats()
        elif page_name == "InventoryPage":
            frame.load_inventory()
        elif page_name == "ReceiptPage":
            frame.load_products()


if __name__ == "__main__":
    app = BoutiqueApp()
    app.mainloop()
