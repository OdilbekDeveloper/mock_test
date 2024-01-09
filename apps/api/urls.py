from django.urls import path, include
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token/', obtain_auth_token, name='token'),

    path('register/', User_Register, name='register'),
    path('login/', User_Login, name='login'),
    path('get_user_data/<int:pk>/', Get_User_Data, name='get-user-data'),
    path('get_results/<int:pk>/', Get_Results, name='get-results'),
    path('get/test_details/', Get_Test_Details),
    path('edit/user/', Edit_User),
    path('speakingtest/create/<int:pk>/', Create_SpeakingTest),
    path('essays/get/unchecked/<int:pk>/', Get_Writing_answers),
    path('users/get/writing/unchecked/', get_users_with_unchecked_writing),
    path('writing_test/create/<int:user_id>/<int:section1_id>/<int:section2_id>/<int:answer1_id>/<int:answer2_id>/', Create_writing_test),
    path('check-all-answers/', CheckAllAnswers),
    path('speaking_section/<int:pk>/', Get_Speaking),


    path('adminlist/<int:pk>/', Get_AdminList),
    path('filter_candidates/<int:pk>/', Filter_Candidates),
    path('statistics/', Statistics),
    path('send-message/', Send_Message),
    
    # path('paycom/', TestView.as_view()),
    # path('payme/', Payme),

    path('check/username/exists/<str:username>/', Check_Username_Exists),
    path('payment/add/', Add_Payment),
    path('referral/add/<int:pk>/', Add_refferal),

    # path('payments/merchant/', PaymeCallBackAPIView.as_view()),
    # path('payments/generate/link/', Generate_Pay_Link),
    # path('payments/generate/link/2/', Generate_Pay_Link),
    # path("payments/", include("payme.urls"))
]
