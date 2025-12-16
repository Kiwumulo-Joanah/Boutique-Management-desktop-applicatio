# JK's Boutique - User Guide

## Getting Started

### For New Users

1. **Launch the Application**
   - Run `run_app.bat` or execute `python main.py`

2. **Create Your Account**
   - Click on "Register here" link on the login page
   - Fill in all required fields:
     - Full Name
     - Email Address
     - Username (minimum 3 characters)
     - Password (minimum 6 characters)
     - Confirm Password
   - Click "Register" button
   - You will be redirected to the login page

3. **Login**
   - Enter your username and password
   - Click "Login" to access the dashboard

### Default Admin Access

For immediate access, use the default owner account:
- **Username:** owner
- **Password:** admin123

## Application Features

### 1. Dashboard
- View total number of products
- Check total inventory value
- Monitor low stock items (less than 10 units)
- Navigate to other features

### 2. Add New Stock
- Enter product name
- Set price in UGX (Ugandan Shillings)
- Specify quantity
- Click "Add Product" to save

### 3. Inventory Management
- View all products in a table format
- See product ID, name, price, quantity, and total value
- Delete products by selecting them and clicking "Delete Selected"
- Refresh the list to see updated data

### 4. Generate Receipt
- Select a product from the dropdown
- Enter quantity to sell
- Add multiple items to cart
- Review total amount
- Click "Generate Receipt" to create PDF
- Receipt automatically updates inventory

## Security Features

- Password protection for all accounts
- Separate user account management
- Secure login validation

## Data Management

- **Inventory Data:** Automatically saved to `inventory.json`
- **User Accounts:** Stored securely in `users.json`
- **Receipts:** Generated as PDF files with unique timestamps

## Tips

1. **Keep Track of Stock:** Regularly check the dashboard for low stock alerts
2. **Backup Data:** Periodically backup your `inventory.json` and `users.json` files
3. **Receipt Storage:** Organize generated receipt PDFs in a separate folder
4. **Multiple Users:** Each staff member can have their own account

## Troubleshooting

### Cannot Login
- Verify username and password are correct
- Check if Caps Lock is on
- Try the default owner account

### Receipt Not Generating
- Ensure cart has items
- Check if sufficient stock is available
- Verify reportlab is installed: `pip install reportlab`

### Data Not Saving
- Check file permissions in the application directory
- Ensure `inventory.json` and `users.json` are not opened in another program

## Support

For issues or questions about the application, contact the system administrator.

---
**JK's Boutique and Kid's Wear** - Inventory Management System
Version 1.0 | December 2025
