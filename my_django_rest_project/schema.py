import graphene
from graphene_django import DjangoObjectType
from rbac.models import User, Role, Menu,ABC
#from common.schema import Query as CommonQuery
from django.contrib.auth.models import Group, Permission
from common.schema import Query as CommonQuery, Mutation as CommonMutation
# --- Generic Factory (Supports Open/Closed and DRY) ---
def create_django_object_type(model, fields='__all__'):
    """Generic factory to create DjangoObjectType classes dynamically."""
    return type(f'{model.__name__}Type', (DjangoObjectType,), {
        'Meta': type('Meta', (), {'model': model, 'fields': fields})
    })

# Dynamically generate types using the generic factory
RoleType = create_django_object_type(Role)
MenuType = create_django_object_type(Menu)
PermissionType = create_django_object_type(Permission, fields=['id', 'name', 'codename', 'content_type'])
GroupType = create_django_object_type(Group)
UserType = create_django_object_type(User)  # Replaced manual UserType definition
ABCType = create_django_object_type(ABC, fields=["id", "name", "description", "created_at"])

# --- Query Classes (Single Responsibility Principle) ---
class UserQuery(graphene.ObjectType):
    """Handles only user-related queries."""
    all_users = graphene.List(UserType)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

class RoleQuery(graphene.ObjectType):
    """Handles only role-related queries."""
    all_roles = graphene.List(RoleType)

    def resolve_all_roles(self, info, **kwargs):
        return Role.objects.all()

class MenuQuery(graphene.ObjectType):
    """Handles only menu-related queries."""
    all_menus = graphene.List(MenuType)

    def resolve_all_menus(self, info, **kwargs):
        return Menu.objects.all()

class PermissionQuery(graphene.ObjectType):
    """Handles only permission-related queries."""
    all_permissions = graphene.List(PermissionType)

    def resolve_all_permissions(self, info, **kwargs):
        return Permission.objects.all()

class GroupQuery(graphene.ObjectType):
    """Handles only group-related queries."""
    all_groups = graphene.List(GroupType)

    def resolve_all_groups(self, info, **kwargs):
        return Group.objects.all()

class ABCQuery(graphene.ObjectType):
    """Handles only group-related queries."""
    all_abc = graphene.List(ABCType)

    def resolve_all_abcs(self, info, **kwargs): # Resolver for ABC
        return ABC.objects.all()
# --- Combine Queries (Interface Segregation) ---
class Query(    
    UserQuery,
    RoleQuery,
    MenuQuery,
    PermissionQuery,
    GroupQuery,
    ABCQuery,
    CommonQuery,
    graphene.ObjectType,
):
    """Aggregates all query classes into a single Query schema."""
    pass

# --- Mutation Design (Open/Closed and Single Responsibility) ---
class CreateUser(graphene.Mutation):
    """Handles user creation with minimal required fields."""
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email):
        user = User(username=username, email=email)
        user.save()
        return CreateUser(user=user)
class CreateABC(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    abc = graphene.Field(ABCType)

    def mutate(self, info, name, description=None):
        abc = ABC.objects.create(name=name, description=description)
        return CreateABC(abc=abc)

# Additional mutations can be added as separate classes here

class Mutation(CommonMutation,graphene.ObjectType):
    """Aggregates all mutations."""
    # create_user = CreateUser.Field()
    # create_abc = CreateABC.Field()  # New Mutation
    
    pass

# --- Schema Configuration ---
schema = graphene.Schema(query=Query, mutation=Mutation)