"""
Test Receipt Generation
This script tests if the receipt generation is working
"""

import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def get_receipts_folder():
    """Get the receipts folder path"""
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
        print(f"✅ Created receipts folder: {receipts_folder}")
    else:
        print(f"✅ Receipts folder exists: {receipts_folder}")
    
    return receipts_folder

def test_receipt_generation():
    """Test generating a sample receipt"""
    print("\n" + "="*60)
    print("TESTING RECEIPT GENERATION")
    print("="*60)
    
    try:
        # Get receipts folder
        receipts_folder = get_receipts_folder()
        
        # Create test data
        items = [
            {'name': 'Kids T-Shirt', 'quantity': 2, 'price': 15000, 'subtotal': 30000},
            {'name': 'Kids Dress', 'quantity': 1, 'price': 35000, 'subtotal': 35000}
        ]
        total = 65000
        receipt_number = 1
        
        # Generate filename
        filename = f"receipt_{receipt_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        full_path = os.path.join(receipts_folder, filename)
        
        print(f"\n📄 Creating receipt: {filename}")
        print(f"📁 Full path: {full_path}")
        
        # Create PDF
        c = canvas.Canvas(full_path, pagesize=letter)
        width, height = letter
        
        # Header
        c.setFont("Helvetica-Bold", 20)
        c.drawString(1*inch, height - 1*inch, "JK's Boutique and Kid's Wear")
        
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 1.3*inch, f"Receipt Number: {receipt_number}")
        c.drawString(1*inch, height - 1.5*inch, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Line
        c.line(1*inch, height - 1.7*inch, width - 1*inch, height - 1.7*inch)
        
        # Items header
        y_position = height - 2*inch
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1*inch, y_position, "Product")
        c.drawString(3.5*inch, y_position, "Quantity")
        c.drawString(4.5*inch, y_position, "Price")
        c.drawString(5.5*inch, y_position, "Subtotal")
        
        # Items
        c.setFont("Helvetica", 11)
        y_position -= 0.3*inch
        for item in items:
            c.drawString(1*inch, y_position, item['name'][:25])
            c.drawString(3.5*inch, y_position, str(item['quantity']))
            c.drawString(4.5*inch, y_position, f"UGX {item['price']:,.0f}")
            c.drawString(5.5*inch, y_position, f"UGX {item['subtotal']:,.0f}")
            y_position -= 0.25*inch
        
        # Total
        y_position -= 0.2*inch
        c.line(1*inch, y_position, width - 1*inch, y_position)
        y_position -= 0.3*inch
        c.setFont("Helvetica-Bold", 14)
        c.drawString(4.5*inch, y_position, "TOTAL:")
        c.drawString(5.5*inch, y_position, f"UGX {total:,.0f}")
        
        # Footer
        c.setFont("Helvetica-Italic", 10)
        c.drawString(1*inch, 1*inch, "Thank you for shopping with us!")
        
        c.save()
        
        print(f"\n✅ SUCCESS! Receipt generated successfully!")
        print(f"📁 Location: {full_path}")
        print(f"📏 File size: {os.path.getsize(full_path)} bytes")
        
        # Verify file exists
        if os.path.exists(full_path):
            print(f"✅ File verified: EXISTS")
        else:
            print(f"❌ ERROR: File does not exist!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🧪 RECEIPT GENERATION TEST")
    print("="*60)
    
    success = test_receipt_generation()
    
    print("\n" + "="*60)
    if success:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ TESTS FAILED!")
    print("="*60)
    
    input("\nPress Enter to exit...")
