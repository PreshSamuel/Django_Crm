from django.urls import path
from .views import Home, Logout_user, Signup, Customer_record, Delete_record, add_record, Update_record

app_name = 'crm_main_app'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('logout', Logout_user.as_view(), name='logout'),
    path('signup/', Signup.as_view(), name='signup'),
    path('record/<int:pk>', Customer_record.as_view(), name='record'),
    path('delete_record/<int:pk>', Delete_record.as_view(), name='delete_record'),
    path('update_record/<int:pk>', Update_record.as_view(), name='update_record'),
    path('add_record/', add_record, name='add_record'),
]