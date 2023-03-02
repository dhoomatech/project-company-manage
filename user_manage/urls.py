from django.urls import path
from .views import *

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('account-login', AccountLogin.as_view()),
    path('admin-account-login', AdminAccountLogin.as_view()),
    path('create-manager', CreateManagerAccount.as_view()),
    path('create-company', CreateCompanyAccount.as_view()),
    path('update-company', UpdateCompanyAccount.as_view()),

    path('admin-company-list', AdminCompanyList.as_view()),
    path('admin-manager-list', AdminManagerList.as_view()),

    path('company-list', CompanyList.as_view()),

    path('employee-list', EmployeeList.as_view()),
    path('employee-create', CreateEmployee.as_view()),
    path('employee-update', UpdateEmployee.as_view()),

    path('company-manager-documents', AccountDocumentUpload.as_view()),

    path('user-profile-update', UpdateDataProfile.as_view()),

    path('employee-documents/<int:emp_id>', EmployeeDocumentUpload.as_view()),
    path('company-documents/<int:company_id>', CompanyDocuments.as_view()),


    # path('account-login-verify/<str:user_type>', CustomAuthToken.as_view()),
]
