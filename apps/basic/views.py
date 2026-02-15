# from django.shortcuts import redirect
# from rest_framework.generics import CreateAPIView
# from apps.basic import serializers
# from apps.basic.models import ClickOrder
# from pyclick import PyClick
# from pyclick.views import PyClickMerchantAPIView
# from rest_framework.response import Response
# from apps.main.models import User
# import requests
# from apps.main.models import Test_Details
# from apps.basic.serializers import TestDetailSerializer
# from rest_framework.decorators import api_view
# from django.http import JsonResponse
# class CreateClickOrderView(CreateAPIView):
#     serializer_class = serializers.ClickOrderSerializer
#
#     def post(self, request, *args, **kwargs):
#         amount = request.POST.get('amount')
#         telegram_id = request.POST.get('telegram_id')
#
#         user = User.objects.get(telegram_id=telegram_id)
#         order = ClickOrder.objects.create(amount=amount, user=user)
#         return_url = 'https://t.me/ieltsplus_bot'
#         url = PyClick.generate_url(order_id=order.id, amount=str(amount), return_url=return_url)
#
#         data = {
#             'url': url,
#         }
#         return JsonResponse(data)
#
#
# class OrderCheckAndPayment(PyClick):
#     def check_order(self, order_id: str, amount: str):
#         if order_id:
#             try:
#                 order = ClickOrder.objects.get(id=order_id)
#                 if int(amount) == order.amount:
#                     return self.ORDER_FOUND
#                 else:
#                     return self.INVALID_AMOUNT
#             except ClickOrder.DoesNotExist:
#                 return self.ORDER_NOT_FOUND
#
#     def successfully_payment(self, order_id: str, transaction: object):
#         """ Эта функция вызывается после успешной оплаты """
#         try:
#             prices = Test_Details.objects.last()
#             order = ClickOrder.objects.get(id=order_id)
#             order.is_paid = True
#             order.save()
#
#             if order.amount == prices.price2:
#                 user = order.user
#                 user.balance += int(prices.price2)
#                 user.save()
#             elif order.amount == prices.price4:
#                 user = order.user
#                 user.balance += int(prices.price4)
#                 user.save()
#             elif order.amount == prices.price10:
#                 user = order.user
#                 user.balance += int(prices.price10)
#                 user.save()
#             else:
#                 user = order.user
#                 user.balance += order.amount
#                 user.save()
#
#             token = '6417593875:AAFelHT9VtJxaJ9F7tm4Bihd-uR5zMG1df4'
#             url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id='
#             text = f"You have received {order.amount}sum in your balance via Click app"
#             requests.get(url + str(user.telegram_id) + '&text=' + text)
#         except ClickOrder.DoesNotExist:
#             print(f"no order object not found: {order_id}")
#
#
# class OrderTestView(PyClickMerchantAPIView):
#     VALIDATE_CLASS = OrderCheckAndPayment
#
# @api_view(['GET'])
# def TestView(request):
#     prices = Test_Details.objects.last()
#     print(prices)
#     ser = TestDetailSerializer(prices)
#
#     return Response(ser.data)
#




from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse

from apps.basic import serializers
from apps.basic.models import ClickOrder
from apps.main.models import User, Test_Details
from apps.basic.serializers import TestDetailSerializer

import requests


# ✅ CREATE ORDER (FAKE PAYMENT LINK)
class CreateClickOrderView(CreateAPIView):
    serializer_class = serializers.ClickOrderSerializer

    def post(self, request, *args, **kwargs):
        amount = int(request.POST.get('amount'))
        telegram_id = request.POST.get('telegram_id')

        user = User.objects.get(telegram_id=telegram_id)
        order = ClickOrder.objects.create(amount=amount, user=user)

        # 🔥 Fake payment URL for demo
        fake_payment_url = f"/demo-payment-success/?order_id={order.id}"

        return JsonResponse({'url': fake_payment_url})


# ✅ DEMO PAYMENT HANDLER (NO REAL GATEWAY)
class DemoPaymentSuccessView(APIView):
    def get(self, request, *args, **kwargs):
        order_id = request.GET.get("order_id")

        try:
            order = ClickOrder.objects.get(id=order_id)
            if order.is_paid:
                return Response({"status": "already paid"})

            order.is_paid = True
            order.save()

            prices = Test_Details.objects.last()
            user = order.user

            # Add balance based on pricing tiers
            if prices:
                if order.amount == prices.price2:
                    user.balance += int(prices.price2)
                elif order.amount == prices.price4:
                    user.balance += int(prices.price4)
                elif order.amount == prices.price10:
                    user.balance += int(prices.price10)
                else:
                    user.balance += order.amount
            else:
                user.balance += order.amount

            user.save()

            # 🔔 Telegram notification (optional, safe)
            try:
                token = 'PASTE_YOUR_TELEGRAM_BOT_TOKEN_IF_NEEDED'
                text = f"You received {order.amount} sum in demo balance"
                requests.get(
                    f'https://api.telegram.org/bot{token}/sendMessage',
                    params={'chat_id': user.telegram_id, 'text': text},
                    timeout=3
                )
            except Exception:
                pass

            return Response({"status": "demo payment success"})

        except ClickOrder.DoesNotExist:
            return Response({"error": "order not found"}, status=404)


# ✅ SIMPLE TEST PRICE API
@api_view(['GET'])
def TestView(request):
    prices = Test_Details.objects.last()
    ser = TestDetailSerializer(prices)
    return Response(ser.data)
