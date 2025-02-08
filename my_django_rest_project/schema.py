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
    permissions = graphene.List(PermissionType)

    class Meta:
        model = Group
        fields = '__all__'
    def resolve_permissions(self, info):
        return self.permissions.all()
        #return [permission.id for permission in self.permissions.all()]

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

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_all_roles(self, info, **kwargs):
        return Role.objects.all()

    def resolve_all_menus(root, info):
        return Menu.objects.all()

    def resolve_all_permissions(self, info, **kwargs):
        return Permission.objects.all()

    def resolve_all_groups(self, info, **kwargs):
        return Group.objects.all()
    
class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, username, email):
        user = User(username=username, email=email)
        user.save()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)