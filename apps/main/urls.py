from django.urls import path
from .views import *
urlpatterns = [
    path('login/', Login_Page),

    path('listening_section/<int:pk>/', Get_Listening_Section, name='listening_section'),
    path('add/listening/', add_listening_answers, name='listening-add'),


    path('reading_section/<int:pk>/', Get_Reading_Section),
    path('add/reading/', add_reading_answers, name='reading-add'),

    path('writing_section/<int:pk>/', Get_Writing_Section),
    path('add/writing/', Add_writing_answers, name='writing-add'),
    path('finished/', Finished_Writing_Page),

]
