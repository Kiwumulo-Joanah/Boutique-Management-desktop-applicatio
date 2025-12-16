# Testing Checklist for JK's Boutique Application

## ✅ Pre-Launch Checklist

### Installation
- [ ] Python is installed (version 3.7+)
- [ ] Required packages installed: `pip install reportlab pyinstaller`
- [ ] All files present:
  - [ ] main.py
  - [ ] run_app.bat
  - [ ] build_exe.bat
  - [ ] requirements.txt
  - [ ] README.md

---

## 🧪 Feature Testing

### 1. Registration Page Testing
- [ ] **Launch Application**
  - [ ] Application window opens successfully
  - [ ] Registration link visible on login page

- [ ] **Form Validation**
  - [ ] Error shown when fields are empty
  - [ ] Error shown when username < 3 characters
  - [ ] Error shown when password < 6 characters
  - [ ] Error shown when passwords don't match
  - [ ] Error shown for invalid email format
  - [ ] Error shown for duplicate username

- [ ] **Successful Registration**
  - [ ] Can enter all fields correctly
  - [ ] Success message appears
  - [ ] Redirects to login page
  - [ ] User saved in users.json
  - [ ] Form clears after registration

### 2. Login Page Testing
- [ ] **Default Owner Account**
  - [ ] Can login with username: owner, password: admin123
  - [ ] Redirects to dashboard

- [ ] **Registered User Login**
  - [ ] Can login with newly registered account
  - [ ] Error shown for invalid credentials
  - [ ] Password is masked with asterisks
  - [ ] Enter key triggers login

- [ ] **Navigation**
  - [ ] "Register here" link works
  - [ ] Returns to login from registration

### 3. Dashboard Testing
- [ ] **Statistics Display**
  - [ ] Total products count is accurate
  - [ ] Total inventory value calculated correctly
  - [ ] Low stock items count correct (items < 10)
  - [ ] Statistics update when returning to dashboard

- [ ] **Navigation Buttons**
  - [ ] "Add New Stock" button works
  - [ ] "View Inventory" button works
  - [ ] "Generate Receipt" button works
  - [ ] "Logout" button returns to login

### 4. Add Stock Page Testing
- [ ] **Form Functionality**
  - [ ] Product name accepts text
  - [ ] Price accepts numbers only
  - [ ] Quantity accepts integers only
  - [ ] Error shown for empty fields
  - [ ] Error shown for negative values

- [ ] **Add Product**
  - [ ] Product added successfully
  - [ ] Success message appears
  - [ ] Product saved to inventory.json
  - [ ] Form clears after adding
  - [ ] Auto-increment ID works
  - [ ] "Back to Dashboard" button works

### 5. Inventory Page Testing
- [ ] **Display Products**
  - [ ] All products shown in table
  - [ ] Columns: ID, Name, Price, Quantity, Total Value
  - [ ] Values formatted correctly (commas in numbers)
  - [ ] Scrollbar works for many items

- [ ] **Refresh Function**
  - [ ] "Refresh" button updates table
  - [ ] New products appear after refresh

- [ ] **Delete Function**
  - [ ] Can select a product
  - [ ] Confirmation dialog appears
  - [ ] Product removed from table
  - [ ] Product removed from inventory.json
  - [ ] Warning shown if nothing selected

### 6. Receipt Page Testing
- [ ] **Product Selection**
  - [ ] Dropdown shows all products
  - [ ] Shows product ID and stock level
  - [ ] Can enter quantity

- [ ] **Add to Cart**
  - [ ] Product added to cart list
  - [ ] Quantity validated (must be > 0)
  - [ ] Error if quantity exceeds stock
  - [ ] Cart displays: name, quantity, subtotal
  - [ ] Total updates automatically

- [ ] **Cart Management**
  - [ ] Can add multiple different products
  - [ ] Total calculates correctly
  - [ ] "Clear Cart" removes all items
  - [ ] Total resets to 0

- [ ] **Generate Receipt**
  - [ ] PDF file created
  - [ ] Filename includes receipt number and timestamp
  - [ ] PDF contains all cart items
  - [ ] PDF shows correct total
  - [ ] PDF has company header
  - [ ] Inventory updated after generation
  - [ ] Cart cleared after generation
  - [ ] Success message shows filename

---

## 📊 Data Persistence Testing
- [ ] **inventory.json**
  - [ ] File created automatically
  - [ ] Products saved correctly
  - [ ] Products loaded on app restart
  - [ ] Updates persist after closing app

- [ ] **users.json**
  - [ ] File created automatically
  - [ ] Users saved correctly
  - [ ] Users loaded on app restart
  - [ ] Can login after app restart

- [ ] **Receipt PDFs**
  - [ ] Files saved in application directory
  - [ ] PDFs can be opened
  - [ ] Content is readable

---

## 🔧 Error Handling Testing
- [ ] Application handles missing data files gracefully
- [ ] Application handles corrupted JSON files
- [ ] Proper error messages for user mistakes
- [ ] No crashes during normal operation

---

## 🎨 UI/UX Testing
- [ ] All text is readable
- [ ] Buttons are clearly labeled
- [ ] Colors are consistent
- [ ] Layout is professional
- [ ] Window is resizable
- [ ] Forms are easy to use

---

## 🏗️ Build Testing (Optional)
- [ ] Run `build_exe.bat` successfully
- [ ] Executable created in dist folder
- [ ] Executable runs without Python installed
- [ ] All features work in executable

---

## 📝 Documentation Testing
- [ ] README.md is clear and accurate
- [ ] USER_GUIDE.md covers all features
- [ ] Sample data script works
- [ ] All credentials documented

---

## Test Results Summary

**Date Tested:** _______________
**Tested By:** _______________
**Test Environment:** Windows ___

**Overall Status:**
- [ ] All tests passed ✅
- [ ] Minor issues found ⚠️
- [ ] Major issues found ❌

**Notes:**
_____________________________________________
_____________________________________________
_____________________________________________

---

**Signature:** ________________  **Date:** ____________
