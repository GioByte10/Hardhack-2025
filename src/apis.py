# Importing library 
import cv2 
from pyzbar.pyzbar import decode 
import matplotlib.pyplot as plt

# Make one method to decode the barcode 
def readBarcodes(image, debug = False):      
    
    # Decode the barcode image 
    detectedBarcodes = decode(image)
    bars = []
    
    # If not detected then print the message 
    if not detectedBarcodes: 
#        print("Barcode Not Detected or your barcode is blank/corrupted!")
        return []
    else: 
        
        # Traverse through all the detected barcodes in image 
        for barcode in detectedBarcodes:
            if barcode.type == 'EAN13':
                bars.append(barcode.data.decode())
                if debug:
                    # Locate the barcode position in image 
                    (x, y, w, h) = barcode.rect 
                    
                    # Put the rectangle in image using 
                    # cv2 to highlight the barcode 
                    cv2.rectangle(image, (x-10, y-10), 
                                (x + w+10, y + h+10), 
                                (255, 0, 0), 2) 
                    print(barcode.data, barcode.type) 
#    print(bars)
    return bars # return the barcode
    
    
def find_item(upc):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False, slow_mo=4000)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")  
        page = context.new_page()
        link = f"https://www.barcodelookup.com/{upc}"
        print(f'going to {link}')
        page.goto(link)
        soup = BeautifulSoup(page.content(), 'html.parser')
        try:
            browser.close()
            return soup.find(class_ = 'col-50 product-details').find('h4').text.strip()
        except:
            return None
