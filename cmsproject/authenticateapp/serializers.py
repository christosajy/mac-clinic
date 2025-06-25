from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class SignupSerializer(serializers.ModelSerializer):
    group_id = serializers.IntegerField(write_only=True, required=False)
    role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'group_id', 'role']

    def create(self, validated_data):
        group_id = validated_data.pop("group_id", None)
        validated_data['password'] = make_password(validated_data.get('password'))
        user = super().create(validated_data)

        if group_id:
            try:
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
            except Group.DoesNotExist:
                raise serializers.ValidationError({"group_id": "Invalid group ID"})

        Token.objects.create(user=user)
        return user

    def get_role(self, obj):
        group = obj.groups.first()
        return group.name if group else None


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid username or password.")
