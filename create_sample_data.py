"""
Test Script for JK's Boutique Application
This script demonstrates the key features
"""

import json
import os

def create_sample_data():
    """Create sample data for testing"""
    
    # Sample products
    sample_products = [
        {"product_id": 1, "name": "Kids T-Shirt (Blue)", "price": 15000, "quantity": 25},
        {"product_id": 2, "name": "Kids T-Shirt (Pink)", "price": 15000, "quantity": 30},
        {"product_id": 3, "name": "Kids Dress", "price": 35000, "quantity": 15},
        {"product_id": 4, "name": "Kids Shorts", "price": 12000, "quantity": 20},
        {"product_id": 5, "name": "Baby Romper", "price": 25000, "quantity": 8},
        {"product_id": 6, "name": "Kids Jeans", "price": 28000, "quantity": 12},
        {"product_id": 7, "name": "Kids Jacket", "price": 45000, "quantity": 5},
        {"product_id": 8, "name": "Baby Blanket", "price": 30000, "quantity": 18}
    ]
    
    # Sample users
    sample_users = [
        {
            "username": "joanah",
            "password": "boutique123",
            "full_name": "Kiwumulo Joanah",
            "email": "joanah@jkboutique.com"
        },
        {
            "username": "manager",
            "password": "manager456",
            "full_name": "Store Manager",
            "email": "manager@jkboutique.com"
        }
    ]
    
    # Save to files
    with open('inventory.json', 'w') as f:
        json.dump(sample_products, f, indent=4)
    print("✅ Sample inventory data created (inventory.json)")
    
    with open('users.json', 'w') as f:
        json.dump(sample_users, f, indent=4)
    print("✅ Sample user accounts created (users.json)")
    
    print("\n📋 Sample Data Created Successfully!")
    print("\n👥 Test User Accounts:")
    print("   1. Username: owner | Password: admin123 (default)")
    print("   2. Username: joanah | Password: boutique123")
    print("   3. Username: manager | Password: manager456")
    
    print("\n📦 Sample Products Added:")
    for product in sample_products:
        print(f"   - {product['name']}: UGX {product['price']:,} (Stock: {product['quantity']})")
    
    print("\n🚀 Ready to run the application!")
    print("   Run: python main.py")

if __name__ == "__main__":
    print("=" * 60)
    print("JK's Boutique - Test Data Generator")
    print("=" * 60)
    print()
    
    if os.path.exists('inventory.json') or os.path.exists('users.json'):
        response = input("⚠️  Data files already exist. Overwrite? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("❌ Operation cancelled.")
            exit()
    
    create_sample_data()
    print("\n" + "=" * 60)
