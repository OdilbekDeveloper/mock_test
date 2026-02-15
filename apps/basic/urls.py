# from django.urls import path
# from apps.basic import views
# from apps.basic.views import TestView
#
# urlpatterns = [
#     path('', views.CreateClickOrderView.as_view()),
#     path('click/transaction/', views.OrderTestView.as_view()),
#     path('test/', TestView),
# ]


from django.urls import path
from apps.basic import views
from apps.basic.views import TestView, DemoPaymentSuccessView

urlpatterns = [
    path('', views.CreateClickOrderView.as_view(), name='create-order'),
    path('demo-payment-success/', DemoPaymentSuccessView.as_view(), name='demo-payment'),
    path('test/', TestView, name='test-prices'),
]
