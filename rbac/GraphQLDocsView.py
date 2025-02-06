from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

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