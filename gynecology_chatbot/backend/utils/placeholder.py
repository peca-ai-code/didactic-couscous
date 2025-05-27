from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
import io

def placeholder_image(request, width, height):
    """Generate a placeholder image with the specified dimensions."""
    # Create a new image with the specified dimensions
    image = Image.new('RGB', (int(width), int(height)), color=(200, 200, 200))
    
    # Draw the dimensions as text on the image
    draw = ImageDraw.Draw(image)
    text = f"{width}x{height}"
    text_color = (100, 100, 100)
    
    # Calculate text position to center it
    text_width = draw.textlength(text, font=None)
    text_position = ((int(width) - text_width) // 2, int(height) // 2 - 5)
    
    # Draw the text
    draw.text(text_position, text, fill=text_color)
    
    # Create a profile-like circular shape
    if width == height:  # If it's square, draw a circle
        circle_margin = int(width) // 10
        ellipse_box = [circle_margin, circle_margin, 
                      int(width) - circle_margin, int(height) - circle_margin]
        draw.ellipse(ellipse_box, outline=(180, 180, 180), width=2)
    
    # Save the image to a byte buffer
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Return the image
    return HttpResponse(buffer, content_type='image/png')
