from apps.api.models import Payment
from apps.main.models import *
from rest_framework import serializers


class SpeakingSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaking_section
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class FullTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Full_test
        fields = "__all__"
        depth = 1


class TestDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_Details
        fields = "__all__"


class SpeakingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaking_test
        fields = "__all__"


class WritingAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writing_answer
        fields = "__all__"
        depth = 2


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        depth = 1