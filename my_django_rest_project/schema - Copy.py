import graphene
from graphene_django import DjangoObjectType
from rbac.models import User, Role, Menu
from django.contrib.auth.models import Group, Permission

def create_django_object_type(model, fields='__all__'):
    return type(f'{model.__name__}Type', (DjangoObjectType,), {
        'Meta': type('Meta', (), {'model': model, 'fields': fields})
    })

RoleType = create_django_object_type(Role)
MenuType = create_django_object_type(Menu)
PermissionType = create_django_object_type(Permission, fields=['id', 'name', 'codename', 'content_type'])
GroupType = create_django_object_type(Group)

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

    def resolve_all_menus(self, info, **kwargs):
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
