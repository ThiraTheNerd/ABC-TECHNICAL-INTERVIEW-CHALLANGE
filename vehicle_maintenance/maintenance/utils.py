from PIL import Image  # For image processing
import io  # For in-memory file storage
from django.core.files.base import ContentFile  # For creating Django files

def compress_image(image):
    # Open the uploaded image
    img = Image.open(image)
    img = img.convert('RGB')  # Ensure it's in RGB format
    
    # Create an in-memory file to store the compressed image
    compressed_io = io.BytesIO()
    
    # Compress the image and save it to the in-memory file
    img.save(compressed_io, format='JPEG', quality=70)  # Set quality (e.g., 70%)
    
    # Create a Django file from the in-memory file
    compressed_image = ContentFile(compressed_io.getvalue(), name=image.name)
    
    return compressed_image
