from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

class SignupSerializer(serializers.ModelSerializer):
    group_id = serializers.IntegerField(write_only=True, required=False)
    role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'group_id', 'role']
        extra_kwargs = {'password': {'write_only': True}}

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
        return user

    def get_role(self, obj):
        group = obj.groups.first()
        return group.id if group else None

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
