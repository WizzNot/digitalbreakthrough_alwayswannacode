from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
import uuid
from tensorflow.keras.preprocessing import image
import numpy as np
from django.conf import settings


def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img = image.img_to_array(img, dtype=np.uint8)
    img = np.expand_dims(img, axis=0)  # Добавляем размерность батча
    return img



def home(request):
    template = "homepage/home.html"
    return render(request, template_name=template)


def upload(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        unique_filename = str(uuid.uuid4()) + os.path.splitext(image_file.name)[-1]
        fs = FileSystemStorage()
        fs.save("images/" + unique_filename, image_file)
        image = preprocess_image("images/" + unique_filename)
        group_index = settings.MODEL.predict(preprocess_image("images/" + unique_filename))
        return render(request, 'homepage/upload_success.html', {"category": settings.GROUPS[np.where(group_index[0] == 1.)[0][0]]})
    return render(request, 'homepage/upload_fail.html')