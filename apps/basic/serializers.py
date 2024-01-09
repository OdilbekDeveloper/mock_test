from rest_framework import serializers
from .models import ClickOrder
from apps.main.models import Test_Details

class ClickOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickOrder
        fields = ["amount", "is_paid"]



class TestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_Details
        fields = "__all__"