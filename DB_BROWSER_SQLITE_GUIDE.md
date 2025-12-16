# 🗄️ DB Browser for SQLite - Connection Guide

## What is DB Browser for SQLite?

DB Browser for SQLite is a free, open-source visual tool to:
- View your database tables
- Browse all data (products, users, receipts)
- Run SQL queries
- Export data
- Manage database structure

---

## 📥 Download & Install

### Step 1: Download

**Website:** https://sqlitebrowser.org/

**Direct Download (Windows):**
https://github.com/sqlitebrowser/sqlitebrowser/releases

Choose: `DB.Browser.for.SQLite-xxx-win64.msi` (latest version)

### Step 2: Install

1. Run the downloaded .msi installer
2. Follow installation wizard
3. Click "Install" (default settings are fine)
4. Click "Finish"

---

## 🔌 Connecting to Your Database

### Method 1: From Running Application

**When running as Python script:**
```
Database location: c:\Users\JUDICIARY\Desktop\KIWUMULO JOANAH\boutique.db
```

**When running as executable:**
```
Database location: c:\Users\JUDICIARY\Desktop\KIWUMULO JOANAH\dist\boutique.db
```

### Method 2: Open in DB Browser

1. **Launch DB Browser for SQLite**
2. Click **"Open Database"** button (or File → Open Database)
3. Navigate to your database location:
   - Python: `c:\Users\JUDICIARY\Desktop\KIWUMULO JOANAH\boutique.db`
   - Executable: `c:\Users\JUDICIARY\Desktop\KIWUMULO JOANAH\dist\boutique.db`
4. Click **"Open"**

✅ **Database Connected!**

---

## 📊 Viewing Your Data

### Database Structure

Your database has **4 tables:**

```
boutique.db
├── products        (Inventory items)
├── users           (Registered users)
├── receipts        (Sales transactions)
└── receipt_items   (Items in each receipt)
```

---

### Table 1: products

**View your inventory:**

1. Click **"Browse Data"** tab
2. Select **"products"** from Table dropdown
3. See all your products!

**Columns:**
- `product_id` - Unique product ID
- `name` - Product name
- `price` - Price in UGX
- `quantity` - Stock quantity

**Example data:**
```
| product_id | name         | price | quantity |
|------------|-------------|-------|----------|
| 1          | Kids T-Shirt | 15000 | 25       |
| 2          | Kids Dress   | 35000 | 15       |
| 3          | Kids Shorts  | 12000 | 20       |
```

---

### Table 2: users

**View registered users:**

1. Click **"Browse Data"** tab
2. Select **"users"** from Table dropdown
3. See all registered users!

**Columns:**
- `user_id` - Unique user ID
- `username` - Login username
- `password` - User password
- `full_name` - User's full name
- `email` - Email address
- `created_at` - Registration date

**Example data:**
```
| user_id | username | password | full_name  | email           | created_at          |
|---------|----------|----------|-----------|-----------------|---------------------|
| 1       | john123  | pass123  | John Doe  | john@email.com | 2025-12-16 14:30:00 |
| 2       | jane456  | pass456  | Jane Smith| jane@email.com | 2025-12-16 15:45:00 |
```

---

### Table 3: receipts

**View sales transactions:**

1. Click **"Browse Data"** tab
2. Select **"receipts"** from Table dropdown
3. See all generated receipts!

**Columns:**
- `receipt_id` - Unique receipt number
- `total` - Total amount
- `filename` - PDF filename
- `created_at` - Date & time of sale

**Example data:**
```
| receipt_id | total  | filename                           | created_at          |
|------------|--------|-----------------------------------|---------------------|
| 1          | 50000  | receipt_1_20251216_143025.pdf     | 2025-12-16 14:30:25 |
| 2          | 75000  | receipt_2_20251216_150530.pdf     | 2025-12-16 15:05:30 |
```

---

### Table 4: receipt_items

**View items in each receipt:**

1. Click **"Browse Data"** tab
2. Select **"receipt_items"** from Table dropdown
3. See detailed breakdown of each sale!

**Columns:**
- `id` - Auto-increment ID
- `receipt_id` - Links to receipts table
- `product_id` - Links to products table
- `product_name` - Product name
- `quantity` - Quantity sold
- `price` - Price at time of sale
- `subtotal` - quantity × price

**Example data:**
```
| id | receipt_id | product_id | product_name | quantity | price | subtotal |
|----|------------|-----------|-------------|----------|-------|----------|
| 1  | 1          | 1         | Kids T-Shirt | 2        | 15000 | 30000    |
| 2  | 1          | 2         | Kids Dress   | 1        | 35000 | 35000    |
| 3  | 2          | 3         | Kids Shorts  | 5        | 12000 | 60000    |
```

---

## 🔍 Running SQL Queries

### Execute SQL Tab

Click **"Execute SQL"** tab to run custom queries.

### Example Queries

#### 1. View All Products
```sql
SELECT * FROM products;
```

#### 2. Low Stock Items (less than 10)
```sql
SELECT * FROM products WHERE quantity < 10;
```

#### 3. Total Inventory Value
```sql
SELECT SUM(price * quantity) AS total_value FROM products;
```

#### 4. All Users Registered Today
```sql
SELECT * FROM users 
WHERE DATE(created_at) = DATE('now');
```

#### 5. Total Sales Today
```sql
SELECT COUNT(*) as receipts, SUM(total) as revenue 
FROM receipts 
WHERE DATE(created_at) = DATE('now');
```

#### 6. Best Selling Products
```sql
SELECT product_name, SUM(quantity) as total_sold
FROM receipt_items
GROUP BY product_name
ORDER BY total_sold DESC;
```

#### 7. Complete Receipt Details
```sql
SELECT r.receipt_id, r.total, r.created_at,
       ri.product_name, ri.quantity, ri.price
FROM receipts r
JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
ORDER BY r.receipt_id DESC;
```

---

## 📤 Exporting Data

### Export to CSV

1. Click **"Browse Data"** tab
2. Select your table
3. Click **"Export"** button
4. Choose **"Export to CSV"**
5. Select location and filename
6. Click **"Save"**

**Use case:** Import into Excel for analysis

---

## 🔧 Database Structure View

### View Table Structure

1. Click **"Database Structure"** tab
2. See all tables listed
3. Expand any table to see:
   - Column names
   - Data types
   - Primary keys
   - Foreign keys

### Example: products table structure
```
Table: products
├── product_id INTEGER PRIMARY KEY AUTOINCREMENT
├── name TEXT NOT NULL
├── price REAL NOT NULL
└── quantity INTEGER NOT NULL
```

---

## ⚠️ Important Notes

### Database Locking

**IMPORTANT:** Close your JK's Boutique application before opening the database in DB Browser!

**Why?** SQLite allows only one write connection at a time.

**If you see "Database locked" error:**
1. Close the JK's Boutique application
2. Try again in DB Browser

### Making Changes

You CAN make changes in DB Browser:
- Add products
- Edit prices
- Delete records
- Add new users

**But be careful!** Changes are immediate and permanent.

### Backup Recommendation

Before making manual changes:
1. Click **"File"** → **"Export"** → **"Database to SQL file"**
2. Save a backup copy
3. Now make your changes safely!

---

## 🎯 Common Tasks

### Task 1: Check User Registrations

**Goal:** See who registered today

**Steps:**
1. Open DB Browser
2. Connect to boutique.db
3. Click "Browse Data" → Select "users"
4. Look at `created_at` column
5. Sort by clicking column header

---

### Task 2: Verify Product Stock

**Goal:** Check current inventory

**Steps:**
1. Open DB Browser
2. Connect to boutique.db
3. Click "Browse Data" → Select "products"
4. View `quantity` column for each product
5. Find low stock items (< 10)

---

### Task 3: View Today's Sales

**Goal:** See all receipts from today

**Steps:**
1. Open DB Browser
2. Connect to boutique.db
3. Click "Execute SQL"
4. Run query:
```sql
SELECT receipt_id, total, created_at 
FROM receipts 
WHERE DATE(created_at) = DATE('now')
ORDER BY created_at DESC;
```
5. Click ▶️ Execute

---

### Task 4: Calculate Total Revenue

**Goal:** Sum all sales

**Steps:**
1. Open DB Browser
2. Connect to boutique.db
3. Click "Execute SQL"
4. Run query:
```sql
SELECT 
    COUNT(*) as total_receipts,
    SUM(total) as total_revenue,
    AVG(total) as average_sale
FROM receipts;
```
5. Click ▶️ Execute

---

## 🆘 Troubleshooting

### Problem: Can't find boutique.db

**Solution:**
- Run your application first (python main.py)
- Database is auto-created on first run
- Location: Same folder as main.py

### Problem: "File is not a database" error

**Solution:**
- Database might be corrupted
- Delete boutique.db
- Run application to create fresh database

### Problem: Empty tables

**Solution:**
- Database is new!
- Add some products via the application
- Register a user
- Generate a receipt
- Then view in DB Browser

### Problem: Can't edit data

**Solution:**
- Check if database is locked
- Close application first
- Make sure you have write permissions

---

## 📚 Learning Resources

### Official DB Browser Documentation
https://github.com/sqlitebrowser/sqlitebrowser/wiki

### SQLite SQL Tutorial
https://www.sqlitetutorial.net/

### Video Tutorials
Search YouTube: "DB Browser for SQLite tutorial"

---

## ✅ Quick Reference

### Open Database
```
File → Open Database → Select boutique.db
```

### Browse Tables
```
Browse Data tab → Select table from dropdown
```

### Run SQL Query
```
Execute SQL tab → Type query → Click Execute
```

### Export Data
```
Browse Data → Export button → CSV/JSON
```

### Close Database
```
File → Close Database
```

---

## 🎉 You're Ready!

Now you can:
- ✅ View all your boutique data
- ✅ Run custom SQL queries
- ✅ Export data for analysis
- ✅ Check inventory and sales
- ✅ Manage users and products

**Open DB Browser and explore your database!**

---

**JK's Boutique - Database Management Made Easy** 🗄️
