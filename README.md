# JK's Boutique and Kid's Wear Application

A desktop application for managing boutique inventory and generating sales receipts.

## 🚀 Version 2.0 - SQLite Edition

### Major Update: Database Integration
- Migrated from JSON to **SQLite database**
- Built-in **Database Browser** (no external tools required!)
- Advanced reporting and analytics
- Better performance and data integrity

## Features

1. **Registration Page** - Create new user accounts with validation
2. **Login Page** - Secure owner and user authentication
3. **Dashboard** - Business overview with statistics
4. **Add Stock Page** - Add new products with name, price, and quantity
5. **Inventory Management Page** - View and manage all products
6. **Receipt Generation Page** - Create sales receipts with automatic PDF generation using ReportLab
7. **Database Browser** - Built-in SQLite database viewer (NEW!)
8. **Reports System** - Receipt history, low stock alerts, inventory reports (NEW!)

## Installation

1. Install Python (if not already installed)
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

```
python main.py
```

## Login Credentials

**Default Owner Account:**
- **Username:** owner
- **Password:** admin123

**New Users:** Can register their own accounts through the registration page

## Creating Executable

To create a standalone executable using PyInstaller:

```
pyinstaller --onefile --windowed --name "JK_Boutique" main.py
```

The executable will be created in the `dist` folder.

## Usage

1. **First Time Users:** Click "Register here" to create a new account with your details
2. **Login:** Use your credentials or the default owner account
3. From the dashboard, you can:
   - View business statistics
   - Add new stock items
   - View and manage inventory
   - Generate receipts for sales

4. Receipts are automatically saved as PDF files with date and time stamps

## Data Storage

- All data stored in **SQLite database** (`boutique.db`)
- Built-in database browser for viewing and querying data
- Backup and export functionality included
- Receipts are saved as PDF files in the application directory

## Documentation

- **README.md** - This file
- **USER_GUIDE.md** - Detailed user manual
- **DATABASE_GUIDE.md** - Complete database documentation (NEW!)
- **TESTING_CHECKLIST.md** - Quality assurance checklist
- **APPLICATION_SUMMARY.md** - Technical overview

## Author

Kiwumulo Joanah
