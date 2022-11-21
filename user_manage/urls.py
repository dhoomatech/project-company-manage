from django.urls import path
from .views import *

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('account-login', AccountLogin.as_view()),
    path('admin-account-login', AdminAccountLogin.as_view()),
    path('create-manager', CreateManagerAccount.as_view()),
    path('create-company', CreateCompanyAccount.as_view()),

    path('admin-company-list', AdminCompanyList.as_view()),
    path('admin-manager-list', AdminManagerList.as_view()),

    path('company-list', CompanyList.as_view()),

    path('employee-list', EmployeeList.as_view()),
    path('employee-create', CreateEmployee.as_view()),

    path('company-manager-documents', AccountDocumentUpload.as_view()),

    path('employee-documents/<emp_id:int>', AccountDocumentUpload.as_view()),


    # path('account-login-verify/<str:user_type>', CustomAuthToken.as_view()),
]
