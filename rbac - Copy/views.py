from django.http import JsonResponse
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import User, Role, Permission, Menu
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, MenuSerializer,GroupSerializer
from django.contrib.auth.models import Permission, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from graphene_django.views import GraphQLView
from graphene import Schema
from my_django_rest_project.schema import schema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    #permission_classes = [IsAuthenticated]

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    #permission_classes = [IsAuthenticated]

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
class PermissionListCreateView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class GraphQLQueryView1(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        query = request.data.get('query')
        result = schema.execute(query)
        return Response(result.data)
    
class GraphQLDocsView1(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        graphql_query = """
        {
          allUsers {
            id
            username
            email
            roles {
              name
            }
            groups {
              name
            }
            userPermissions {
              name
              codename
            }
          }
        }
        """
        return Response({"graphql_query": graphql_query})
class GraphQLQueryView(APIView):
  permission_classes = [AllowAny]

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    print("GraphQLQueryView initialized")
  

  # @swagger_auto_schema(
  #       request_body=openapi.Schema(
  #           type=openapi.TYPE_OBJECT,
  #           properties={
  #               'query': openapi.Schema(type=openapi.TYPE_STRING, description='GraphQL query')
  #           },
  #           required=['query']
  #       ),
  #       responses={200: openapi.Response('GraphQL response')}
  #     )
  #     def post(self, request, *args, **kwargs):
  #         print("GraphQLQueryView post method called")
  #         query = request.data.get('query')
  #         result = schema.execute(query)
  #         if result.errors:
  #             return JsonResponse({'errors': [str(error) for error in result.errors]}, status=400)
  #         return JsonResponse(result.data, safe=False)


  @swagger_auto_schema(
    request_body=openapi.Schema(
      type=openapi.TYPE_OBJECT,
      properties={
        'query': openapi.Schema(type=openapi.TYPE_STRING, description='GraphQL query')
      },
      required=['query']
    ),
    responses={200: openapi.Response('GraphQL response')}
  )
  def post(self, request, *args, **kwargs):
    print("GraphQLQueryView post method called")
    query = request.data.get('query')
    result = schema.execute(query)
    if result.errors:
              return JsonResponse({'errors': [str(error) for error in result.errors]}, status=400)
    return JsonResponse(result.data, safe=False)

    return Response(result.data)
class GraphQLDocsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        graphql_query = """
        {
          allUsers {
            id
            username
            email
            roles {
              name
            }
            groups {
              name
            }
            userPermissions {
              name
              codename
            }
          }
        }
        """
        return Response({"graphql_query": graphql_query})
