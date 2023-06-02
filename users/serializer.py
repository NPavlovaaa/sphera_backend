from rest_framework import serializers

from users.models import User, AdminIncomeChange


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AdminIncomeChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminIncomeChange
        fields = "__all__"
