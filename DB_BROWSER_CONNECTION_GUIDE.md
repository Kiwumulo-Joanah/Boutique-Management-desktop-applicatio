# 🗄️ DB Browser for SQLite - Connection Guide

## What is DB Browser for SQLite?

DB Browser for SQLite is a FREE, open-source tool that allows you to view and manage SQLite databases visually. It's perfect for viewing your boutique's data!

## Download & Installation

### Step 1: Download DB Browser
1. Visit: https://sqlitebrowser.org/
2. Click **"Download"**
3. Choose **Windows installer** (for your Windows PC)
4. Wait for download to complete

### Step 2: Install
1. Double-click the downloaded `.exe` file
2. Follow installation wizard
3. Click **Next → Next → Install → Finish**

## Connecting to Your Boutique Database

### Method 1: Open Database File

1. **Launch DB Browser for SQLite**
2. Click **"Open Database"** button (or File → Open Database)
3. Navigate to your application folder:
   ```
   c:\Users\JUDICIARY\Desktop\KIWUMULO JOANAH\
   ```
4. Select **`boutique.db`**
5. Click **"Open"**

### Method 2: Drag & Drop

1. Open DB Browser for SQLite
2. Drag **`boutique.db`** file from File Explorer
3. Drop it onto DB Browser window
4. Database opens automatically!

## What You'll See

Once connected, you'll see **4 tables**:

### 📦 Products Table
| Column | Description |
|--------|-------------|
| product_id | Unique product ID |
| name | Product name |
| price | Price in UGX |
| quantity | Stock quantity |

### 👤 Users Table
| Column | Description |
|--------|-------------|
| user_id | Unique user ID |
| username | Login username |
| password | User password |
| full_name | Full name |
| email | Email address |
| created_at | Registration date |

### 🧾 Receipts Table
| Column | Description |
|--------|-------------|
| receipt_id | Unique receipt ID |
| receipt_number | Receipt reference |
| date | Sale date |
| total_amount | Total sale amount |

### 📋 Receipt Items Table
| Column | Description |
|--------|-------------|
| item_id | Unique item ID |
| receipt_id | Links to receipt |
| product_name | Product sold |
| quantity | Quantity sold |
| price | Sale price |
| total | Line total |

## Using DB Browser

### View Data
1. Click **"Browse Data"** tab
2. Select table from dropdown
3. View all records in table

### Search Data
1. In Browse Data tab
2. Click in filter box
3. Type search term
4. Results filter automatically

### Execute SQL Queries
1. Click **"Execute SQL"** tab
2. Type SQL query, for example:
   ```sql
   SELECT * FROM products WHERE quantity < 10;
   ```
3. Click **Run** button (▶️)
4. View results below

### Export Data
1. Select table in Browse Data
2. Click **File → Export → Table to CSV**
3. Choose save location
4. Click **Save**

## Example SQL Queries

### View All Products
```sql
SELECT * FROM products ORDER BY name;
```

### Find Low Stock Items
```sql
SELECT * FROM products WHERE quantity < 10;
```

### View All Registered Users
```sql
SELECT username, full_name, email, created_at FROM users ORDER BY created_at DESC;
```

### View Receipt History
```sql
SELECT receipt_number, date, total_amount 
FROM receipts 
ORDER BY date DESC;
```

### View Best Selling Products
```sql
SELECT product_name, SUM(quantity) as total_sold, SUM(total) as total_revenue
FROM receipt_items
GROUP BY product_name
ORDER BY total_sold DESC;
```

### Count Users
```sql
SELECT COUNT(*) as total_users FROM users;
```

### Total Sales Today
```sql
SELECT SUM(total_amount) as today_sales 
FROM receipts 
WHERE date = date('now');
```

## Important Notes

### ⚠️ Database File Location
The database file **`boutique.db`** is created in the same folder as your application:
```
c:\Users\JUDICIARY\Desktop\KIWUMULO JOANAH\boutique.db
```

### ⚠️ Making Changes
- **BE CAREFUL** when editing data in DB Browser
- Changes are saved immediately
- Make backups before making changes
- **TIP:** Use the application's built-in features instead

### 🔒 Security
- The database contains user passwords
- Keep the database file secure
- Don't share it publicly

## Backup Your Database

### Using DB Browser
1. Open your database
2. Click **File → Backup Database**
3. Choose backup location
4. Name it with date: `boutique_backup_2025-12-16.db`
5. Click **Save**

### Manual Backup
Simply copy **`boutique.db`** to a safe location:
```
Copy from: c:\Users\JUDICIARY\Desktop\KIWUMULO JOANAH\boutique.db
Copy to:   c:\Users\JUDICIARY\Desktop\Backups\boutique_backup_2025-12-16.db
```

## Troubleshooting

### Problem: "Database is locked"
**Solution:** Close the boutique application first, then open DB Browser

### Problem: "File not found"
**Solution:** Make sure you've run the application at least once to create the database

### Problem: "No tables visible"
**Solution:** Database hasn't been initialized. Run the application once.

### Problem: "Can't edit data"
**Solution:** 
1. Make sure database isn't open in the application
2. Check file permissions

## Integration with Your Application

### Your Application Uses:
✅ SQLite database engine (built into Python)
✅ Database file: `boutique.db`
✅ 4 normalized tables with relationships
✅ Foreign key constraints enabled
✅ Automatic database creation on first run

### DB Browser Provides:
✅ Visual interface to view data
✅ SQL query execution
✅ Data export capabilities
✅ Database structure visualization
✅ No coding required!

## Why Use DB Browser?

### ✅ Benefits
- **FREE & Open Source**
- **Easy to use** - no SQL knowledge required
- **Powerful** - execute any SQL query
- **Safe** - view data without risk
- **Portable** - works on Windows, Mac, Linux
- **No installation** - portable version available

### 📊 Perfect For:
- Viewing all your products
- Checking registered users
- Analyzing sales data
- Generating reports
- Learning SQL
- Database backup

## Next Steps

1. **Download** DB Browser from https://sqlitebrowser.org/
2. **Install** it on your computer
3. **Run** your boutique application once (creates database)
4. **Open** `boutique.db` in DB Browser
5. **Explore** your data!

## Support Links

- **DB Browser Website:** https://sqlitebrowser.org/
- **Documentation:** https://github.com/sqlitebrowser/sqlitebrowser/wiki
- **SQLite Tutorial:** https://www.sqlitetutorial.net/

---

**Need Help?**
- Check if database file exists
- Make sure application has run at least once
- Close application before opening in DB Browser
- Keep backups of your database!

**Happy Data Exploring! 📊**
