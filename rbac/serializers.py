from rest_framework import serializers
from .models import User, Role, Menu
from django.contrib.auth.models import Permission, Group

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
        #fields = ['id', 'name', 'codename', 'content_type']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    #user_permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
