import graphene
from graphene_django import DjangoObjectType
from rbac.models import User
from django.contrib.auth.models import Group, Permission


def create_django_object_type(model, fields='__all__'):
    
    return type(f'{model.__name__}Type', (DjangoObjectType,), {
        'Meta': type('Meta', (), {'model': model, 'fields': fields})
    })


GroupType = create_django_object_type(Group)
UserType = create_django_object_type(User)  

class UserQuery(graphene.ObjectType):
    """Handles only user-related queries."""
    all_users = graphene.List(UserType)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()



class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"

class CreateUserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    is_active = graphene.Boolean()
    roles = graphene.List(graphene.Int)  # Assuming roles correspond to groups
    groups = graphene.List(graphene.Int)
    user_permissions = graphene.List(graphene.Int)

class CreateUser(graphene.Mutation):
    class Arguments:
        input = CreateUserInput(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, input):
        # Create user first (without Many-to-Many fields)
        user = User.objects.create_user(
            username=input.username,
            email=input.email,
            is_active=input.is_active
        )

        # Assign Many-to-Many relationships
        if input.groups:
            user.groups.set(Group.objects.filter(id__in=input.groups))
        
        if input.roles:
            user.groups.add(*input.roles)


        if input.user_permissions:
            user.user_permissions.set(Permission.objects.filter(id__in=input.user_permissions))

        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

