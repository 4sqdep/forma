import os
from django.utils.text import slugify
from django.utils import timezone



def upload_file(path):
    filename = os.path.basename(path)
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    return os.path.join(path, filename)

