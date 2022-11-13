from rest_framework import serializers
from .models import *
from .functions import *

class ServicesRequestsSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField('get_documents')
    class Meta:
        model = ServicesRequests
        fields = ['id', 'tittle', 'discription', 'status','documents','transaction_id']

    def get_documents(self, obj):
        if obj.documents:
            return image_url_mapping(obj.documents)
        else:
            return []
    