from rest_framework import serializers
from .models import *
from company_app.functions import get_files_info_bulk,generate_urls

class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginUser
        fields = ['id', 'first_name', 'last_name', 'country_code','phone_code','phone_number','expiry_date','created']



class CompanySerializer(serializers.ModelSerializer):
    company_fname = serializers.SerializerMethodField('get_company_fname')
    company_lname = serializers.SerializerMethodField('get_company_lname')
    company_email = serializers.SerializerMethodField('get_company_email')
    company_phone_code = serializers.SerializerMethodField('get_company_phone_code')
    company_phone_number = serializers.SerializerMethodField('get_company_phone_number')
    company_id = serializers.SerializerMethodField('get_company_id')
    manager_id = serializers.SerializerMethodField('get_manager_id')
    class Meta:
        model = ManagerCompany
        fields = ['id','company_id','manager_id','company_fname','company_lname', 'company_email', 'company_phone_code','company_phone_number']

    def get_company_fname(self, obj):
        return obj.company.first_name
    
    def get_company_lname(self, obj):
        return obj.company.last_name

    def get_company_email(self, obj):
        return obj.company.email

    def get_company_phone_code(self, obj):
        return obj.company.phone_code
    
    def get_company_phone_number(self, obj):
        return str(obj.company.phone_number)
    
    def get_company_id(self, obj):
        return obj.company.id
    
    def get_manager_id(self, obj):
        return obj.manager.id


class EmployeeDetailsSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField('get_documents')
    class Meta:
        model = EmployeeDetails
        fields = "__all__"

    def get_documents(self, obj):
        if obj.documents:
            return generate_urls(get_files_info_bulk(obj.documents))
        else:
            return []