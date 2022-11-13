
from .models import *

    
def get_files_info(file_id):
    try:
        file_obj = FileManager.objects.get(id=file_id)
        return file_obj.upload.url
    except Exception as e:
        return ""

def get_files_info_bulk(file_ids):
    try:
        files_urls = list(FileManager.objects.filter(id__in=file_ids).values_list('upload',flat=True).all())
        return files_urls
    except Exception as e:
        return False

def generate_urls(image_list):
    generated_url = []
    for url_value in image_list:
        if type(url_value) == str:
            generated_url.append(settings.STATIC_URL + url_value)
    
    return generated_url

def image_url_mapping(data_list):
    generated_url = []
    for image_dict in data_list:
        if "image" in image_dict:
            image_url = settings.STATIC_URL + image_dict["image"]
            image_dict["image"] = image_url
        generated_url.append(image_dict)
    
    return generated_url