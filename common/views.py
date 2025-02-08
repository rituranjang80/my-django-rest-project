from django.shortcuts import render
from django.http import JsonResponse
from graphene_django.views import GraphQLView
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from my_django_rest_project.schema import schema

# Create your views here.

class GraphQLQueryView(APIView):
    permission_classes = [AllowAny]

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
