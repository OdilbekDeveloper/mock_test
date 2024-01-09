from django.urls import path
from apps.basic import views
from apps.basic.views import TestView

urlpatterns = [
    path('', views.CreateClickOrderView.as_view()),
    path('click/transaction/', views.OrderTestView.as_view()),
    path('test/', TestView),
]