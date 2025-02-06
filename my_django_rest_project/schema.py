import graphene
from graphene_django import DjangoObjectType
from rbac.models import User, Role, Menu
from django.contrib.auth.models import Group, Permission

class RoleType(DjangoObjectType):
    class Meta:
        model = Role
        fields = '__all__'

class MenuType(DjangoObjectType):
    class Meta:
        model = Menu
        fields = '__all__'

class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']

class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        fields = '__all__'

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_roles = graphene.List(RoleType)
    all_menus = graphene.List(MenuType)
    all_permissions = graphene.List(PermissionType)
    all_groups = graphene.List(GroupType)

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_all_roles(root, info):
        return Role.objects.all()

    def resolve_all_menus(root, info):
        return Menu.objects.all()

    def resolve_all_permissions(root, info):
        return Permission.objects.all()

    def resolve_all_groups(root, info):
        return Group.objects.all()

schema = graphene.Schema(query=Query)