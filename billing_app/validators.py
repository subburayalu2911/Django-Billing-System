
import os
from django.core.exceptions import ValidationError



def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1] 
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if ext.lower() not in valid_extensions:
        raise ValidationError(
            'Unsupported file extension. Only PNG, JPG, JPEG, file allowed')