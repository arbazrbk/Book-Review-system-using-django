from django.shortcuts import render
from .models import QRCode
import qrcode
from pyzbar.pyzbar import decode
import os
import PIL
from PIL import Image 
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from pathlib import Path

def generate(request):
    qr_image_url = None
    if request.method == 'POST':
        data = request.POST.get('qr_data')
        mobile_number = request.POST.get('mobile_number')
        
        
        if not mobile_number or len(mobile_number) !=10 or not mobile_number.isdigit():
            return render(request,'scanner/generate.html',{'error':'invalid mobile number'})
        
        
        qr_code =f"{data}|{mobile_number}"
        qr = qrcode.make(qr_code) 
        qr_image_io = BytesIO()
        qr.save(qr_image_io,format='PNG') 
        qr_image_io.seek(0)  
        
        qr_storage_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        fs = FileSystemStorage(location= qr_storage_path,base_url='/media/qr_codes/')
        
        filename = f"{data}_{mobile_number}.png"
        qr_image_content = ContentFile(qr_image_io.read(),name=filename)
        filepath = fs.save(filename, qr_image_content)
        qr_image_url = fs.url(filename)
        
        
        QRCode.objects.create(data=data,mobile_number=mobile_number)
    return render(request,'scanner/generate.html',{'qr_image_url': qr_image_url})

def scan(request):
    # Initialize ALL variables
    error = None
    scanned_data = None
    result = None  # Add this line
    
    if request.method == 'POST' and request.FILES.get('qr_data'):
        mobile_number = request.POST.get('mobile_number')
        qr_image = request.FILES['qr_data']
        
        # Validate mobile number
        if not mobile_number or len(mobile_number) != 10 or not mobile_number.isdigit():
            return render(request, 'scanner/scanner.html', {
                'error': 'invalid mobile number',
                'result': None  # Add result here too
            })
        
        fs = FileSystemStorage()
        filename = fs.save(qr_image.name, qr_image)  # Fixed: filesname -> filename
        image_path = Path(fs.location) / filename
        
        try:
            image = Image.open(image_path)  
            decoded_objects = decode(image)
            
            if decoded_objects:
                qr_content = decoded_objects[0].data.decode('utf-8').strip()
                qr_data, qr_mobile_number = qr_content.split('|')
                
                qr_entry = QRCode.objects.filter(data=qr_data, mobile_number=qr_mobile_number).first()
                
                if qr_entry and qr_mobile_number == mobile_number:
                    result = "Successfully fully scan completed"  # Fixed spelling
                    
                    qr_entry.delete()
                    
                    qr_image_path = settings.MEDIA_ROOT / 'qr_codes' / f"{qr_data}_{qr_mobile_number}.png"
                    
                    if qr_image_path.exists():  # Fixed: exist -> exists
                        qr_image_path.unlink()  # Fixed: unlike -> unlink
                        
                    if image_path.exists():  # Fixed: exist -> exists
                        image_path.unlink()  # Fixed: unlike -> unlink
                
                else:
                    result = "Scan failed: invalid QR code or mobile number mismatch"            
            else:
                error = 'No QR code found in the image'   
                
        except Exception as e:
            error = f"Error scanning QR code: {str(e)}"
           
        finally:
            if image_path.exists():  # Fixed: exist -> exists
                image_path.unlink()  # Fixed: unlike -> unlink
    
    return render(request, 'scanner/scanner.html', {
        'result': result,
        'error': error  # Also return error
    })