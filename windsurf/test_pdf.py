
from PIL import Image
from io import BytesIO
import sys

try:
    # Create a dummy image (simulating the QR code)
    img = Image.new('RGB', (300, 300), color = 'red')
    
    buffer = BytesIO()
    img.save(buffer, format="PDF", resolution=300)
    
    pdf_bytes = buffer.getvalue()
    print(f"PDF generation successful. Size: {len(pdf_bytes)} bytes")
    
    if pdf_bytes.startswith(b"%PDF"):
        print("SUCCESS: Valid PDF header found")
    else:
        print("FAILURE: Invalid PDF header")
        
except Exception as e:
    print(f"PDF generation failed: {e}")
    import traceback
    traceback.print_exc()
