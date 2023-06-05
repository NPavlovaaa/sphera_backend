from rest_framework import serializers

from users.models import User, AdminIncomeChange, Role


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AdminIncomeChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminIncomeChange
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
