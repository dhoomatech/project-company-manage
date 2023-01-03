
from .models import *
from django.db.models.functions import Concat
from django.db.models import Value,F

    
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
        return []

def get_files_id_check(file_ids):
    try:
        files_ids = list(FileManager.objects.filter(id__in=file_ids).values_list('id',flat=True).all())
        return files_ids
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

def get_files_dict(file_ids):
    try:
        files_urls = FileManager.objects.filter(id__in=file_ids).values('upload','id','user_code','folder_name','is_active','expiry_date').order_by('folder_name').all()
        for file_obj in files_urls:
            file_obj['upload'] = settings.MEDIA_URL + file_obj["upload"]
        return files_urls
    except Exception as e:
        import  traceback
        traceback.print_exc()
        return []

def get_files_folder_dict(file_ids):
    try:
        files_urls = FileManager.objects.filter(id__in=file_ids).values('upload','id','user_code','folder_name','is_active','expiry_date').order_by('folder_name').all()
        folder_structure = {}
        for file_obj in files_urls:
            file_obj['upload'] = settings.MEDIA_URL + file_obj["upload"]
            if file_obj['folder_name'] in folder_structure:
                folder_structure[file_obj['folder_name']].append(file_obj)
            else:
                folder_structure[file_obj['folder_name']] = [file_obj]
        return folder_structure
    except Exception as e:
        import  traceback
        traceback.print_exc()
        return []

def get_files_folder_dict_list(file_ids):
    try:
        files_urls = FileManager.objects.filter(id__in=file_ids).values('upload','id','user_code','folder_name','is_active','expiry_date').order_by('folder_name').all()
        folder_structure_list = []
        folder_structure = {}
        for file_obj in files_urls:
            file_obj['upload'] = settings.MEDIA_URL + file_obj["upload"]
            if file_obj['folder_name'] in folder_structure:
                folder_structure[file_obj['folder_name']].append(file_obj)
            else:
                folder_structure[file_obj['folder_name']] = [file_obj]
        for result_obj in folder_structure:
            folder_structure_list.append({"name":result_obj,"value":folder_structure[result_obj]})

        return folder_structure_list
    except Exception as e:
        import  traceback
        traceback.print_exc()
        return []

def folder_files_name_update(file_ids,folder_name):
    try:
        FileManager.objects.filter(id__in=file_ids).update(folder_name=folder_name)
        return True
    except Exception as e:
        return False