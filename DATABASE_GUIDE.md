# SQLite Database Integration Guide

## Database Structure

JK's Boutique application now uses **SQLite** database for data persistence instead of JSON files.

### Database File
- **Filename:** `boutique.db`
- **Location:** Application root directory
- **Type:** SQLite 3

---

## Database Tables

### 1. **products** Table
Stores all product information.

| Column | Type | Description |
|--------|------|-------------|
| product_id | INTEGER | Primary key (auto-increment) |
| name | TEXT | Product name |
| price | REAL | Product price in UGX |
| quantity | INTEGER | Stock quantity |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

**Sample Query:**
```sql
SELECT * FROM products ORDER BY name;
```

### 2. **users** Table
Stores registered user accounts.

| Column | Type | Description |
|--------|------|-------------|
| user_id | INTEGER | Primary key (auto-increment) |
| username | TEXT | Unique username |
| password | TEXT | User password |
| full_name | TEXT | Full name of user |
| email | TEXT | Email address |
| created_at | TIMESTAMP | Registration date |

**Sample Query:**
```sql
SELECT username, full_name, email, created_at FROM users;
```

### 3. **receipts** Table
Stores receipt header information.

| Column | Type | Description |
|--------|------|-------------|
| receipt_id | INTEGER | Primary key (auto-increment) |
| receipt_number | INTEGER | Sequential receipt number |
| total_amount | REAL | Total sale amount |
| filename | TEXT | PDF filename |
| created_at | TIMESTAMP | Receipt generation time |

**Sample Query:**
```sql
SELECT receipt_number, total_amount, created_at 
FROM receipts 
ORDER BY created_at DESC 
LIMIT 10;
```

### 4. **receipt_items** Table
Stores individual items in each receipt.

| Column | Type | Description |
|--------|------|-------------|
| item_id | INTEGER | Primary key (auto-increment) |
| receipt_id | INTEGER | Foreign key to receipts |
| product_id | INTEGER | Foreign key to products |
| product_name | TEXT | Product name snapshot |
| price | REAL | Price at time of sale |
| quantity | INTEGER | Quantity sold |
| subtotal | REAL | Item subtotal |

**Sample Query:**
```sql
SELECT r.receipt_number, ri.product_name, ri.quantity, ri.subtotal
FROM receipt_items ri
JOIN receipts r ON ri.receipt_id = r.receipt_id
ORDER BY r.created_at DESC;
```

---

## Using the Built-in Database Browser

### Access the Browser
1. Run the application
2. Login to the system
3. Click **"Database"** menu → **"Browse Database"**

### Features
- ✅ View all tables (products, users, receipts, receipt_items)
- ✅ Browse table data with scrolling
- ✅ Execute custom SQL queries
- ✅ Real-time data refresh
- ✅ Column names and data types display

### Executing SQL Queries
1. Select a table from the left panel
2. View data in the tree view
3. Use the SQL Query box at the bottom
4. Click "Execute Query" to run custom queries

**Example Queries:**

```sql
-- Get low stock items
SELECT product_id, name, quantity, price 
FROM products 
WHERE quantity < 10 
ORDER BY quantity;

-- Total sales by date
SELECT DATE(created_at) as sale_date, 
       COUNT(*) as num_receipts, 
       SUM(total_amount) as daily_total
FROM receipts 
GROUP BY DATE(created_at)
ORDER BY sale_date DESC;

-- Most sold products
SELECT ri.product_name, 
       SUM(ri.quantity) as total_sold, 
       SUM(ri.subtotal) as total_revenue
FROM receipt_items ri
GROUP BY ri.product_name
ORDER BY total_sold DESC
LIMIT 10;

-- User registration statistics
SELECT COUNT(*) as total_users, 
       MIN(created_at) as first_registration,
       MAX(created_at) as latest_registration
FROM users;
```

---

## Database Operations via Menu

### 1. **Export to JSON**
- Exports current database to JSON files
- Creates: `products_export.json` and `users_export.json`
- Useful for data portability and backup

### 2. **Backup Database**
- Creates a timestamped backup of `boutique.db`
- Format: `boutique_backup_YYYYMMDD_HHMMSS.db`
- Recommended: Backup daily or before major changes

### 3. **Database Info**
- Shows database file location
- Displays database size
- Lists record counts for all tables
- Shows database type and version

---

## External Tools

### DB Browser for SQLite
You can also use external tools to manage the database:

1. **Download:** https://sqlitebrowser.org/
2. **Install** DB Browser for SQLite
3. **Open:** File → Open Database → Select `boutique.db`

**Features:**
- Visual table structure editor
- Data browsing and editing
- SQL execution
- Import/Export functionality
- Database optimization tools

---

## Data Integrity

### Foreign Keys
The application maintains referential integrity:
- `receipt_items.receipt_id` → `receipts.receipt_id`
- `receipt_items.product_id` → `products.product_id`

### Automatic Updates
- Products: `updated_at` timestamp updates on modification
- Receipts: Inventory automatically decremented on sale
- Users: Unique username constraint prevents duplicates

---

## Advantages over JSON

| Feature | SQLite | JSON Files |
|---------|--------|------------|
| **Query Performance** | ✅ Fast with indexes | ❌ Slow, requires full scan |
| **Concurrent Access** | ✅ Supported | ❌ File locking issues |
| **Data Integrity** | ✅ Foreign keys, constraints | ❌ No validation |
| **Transactions** | ✅ ACID compliant | ❌ Manual implementation |
| **Scalability** | ✅ Handles large datasets | ❌ Memory limited |
| **Backup** | ✅ Single file | ❌ Multiple files |
| **Querying** | ✅ SQL (powerful) | ❌ Manual filtering |
| **Reports** | ✅ Complex queries | ❌ Complex code |

---

## Maintenance Tips

### Regular Backups
```sql
-- Check database integrity
PRAGMA integrity_check;

-- Optimize database
VACUUM;

-- Get database statistics
SELECT * FROM sqlite_master WHERE type='table';
```

### Performance Optimization
- Database automatically creates indexes on primary keys
- Consider adding indexes on frequently queried columns
- Use VACUUM periodically to reclaim space

### Security
- **Password Storage:** Currently plain text (⚠️ Not recommended for production)
- **Recommendation:** Use password hashing (bcrypt, argon2) for production
- **File Permissions:** Restrict `boutique.db` access to authorized users

---

## Troubleshooting

### Database Locked Error
**Problem:** "Database is locked"
**Solution:** Close all connections or restart the application

### Corrupted Database
**Problem:** Database won't open
**Solution:** Restore from latest backup

### Missing Tables
**Problem:** Tables don't exist
**Solution:** Application will recreate tables on startup

### Performance Issues
**Problem:** Slow queries
**Solution:** 
```sql
-- Analyze database
ANALYZE;

-- Rebuild database
VACUUM;
```

---

## Migration from JSON

If you have existing JSON files (`inventory.json`, `users.json`):

1. The application now uses SQLite exclusively
2. Old JSON files are not automatically migrated
3. To migrate data:
   - Use "Import from JSON" feature (if implemented)
   - Or manually add data through the application UI

---

## Developer Notes

### Connection Management
- Single database connection throughout application lifetime
- Connection closed on application exit
- Commits after each write operation

### Thread Safety
- Current implementation: Single-threaded
- For multi-threading: Use connection per thread or locks

### Future Enhancements
- [ ] Password hashing
- [ ] Database encryption
- [ ] Audit logging
- [ ] Data export to Excel/CSV
- [ ] Advanced reporting dashboard
- [ ] Automatic backups

---

**Database Integration Complete! ✅**

Your application now has enterprise-grade data management with SQLite!
