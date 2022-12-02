from rest_framework import serializers
from .models import *
from .functions import *

class ServicesRequestsSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField('get_documents')
    class Meta:
        model = ServicesRequests
        fields = ['id', 'tittle', 'discription', 'status','documents','transaction_id']

    def get_documents(self, obj):
        if obj.documents and type(obj.documents) == dict:
            return image_url_mapping(obj.documents)
        else:
            return []
    

class FileManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileManager
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = "__all__"


class ManagerServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerServices
        fields = "__all__"