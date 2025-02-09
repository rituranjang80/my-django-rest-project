import graphene
from graphene_django import DjangoObjectType
from rbac.models import User, Role, Menu,ABC
#from common.schema import Query as CommonQuery
from django.contrib.auth.models import Group, Permission
from common.schema import Query as CommonQuery, Mutation as CommonMutation
from rbac.schema import UserQuery, RoleQuery, MenuQuery, PermissionQuery, GroupQuery, ABCQuery,CreateUser,CreateABC


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

# Additional mutations can be added as separate classes here

class Mutation(CommonMutation,graphene.ObjectType):
    """Aggregates all mutations."""
    create_user = CreateUser.Field()
    create_abc = CreateABC.Field()  # New Mutation
    
    #pass

# --- Schema Configuration ---
schema = graphene.Schema(query=Query, mutation=Mutation)