from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
import uuid


def home(request):
    template = "homepage/home.html"
    return render(request, template_name=template)


def upload(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        unique_filename = str(uuid.uuid4()) + os.path.splitext(image_file.name)[-1]
        fs = FileSystemStorage()
        fs.save("images/" + unique_filename, image_file)

        return render(request, 'homepage/upload_success.html', {"category": "cat"})
    return render(request, 'homepage/upload_fail.html')