from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response#Return response object from API view


from rest_framework import status#List of handy HTTP status codes that we can use when returning responses from our API
from profiles_api import serializers
# Create your views here.

class HelloAPIView(APIView):
    """Test APIView"""

    serializer_class= serializers.HelloSerializer
    #Function for a GET HTTP request
    def get(self, request, format=None):#format parameter is just best practice to include
        """Returns a list of APIView features"""
        an_api_view=[
            'Uses HTTP methods as function (get,post,patch,put,delete)',
            "Is similar to a traditional Django View",
            "Gives you the most control over your application logic",
            "Is mapped manually to URLs",
        ]
        return Response({'message':'Hello', 
                        'an_api_view':an_api_view})#return in JSON format
    def post(self, request):
        """Create a hello message with our name"""
        serializer=self.serializer_class(data=request.data)#retrieve the serializer that we defined in the serializer_class attribute above. We pass in the request data to the class
        if serializer.is_valid():
            name=serializer.validated_data.get('name') #retrieve the name field defined in our serializer
            message=f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )
    def put(self, request, pk=None):#Need pk to identify which object to put
        """Handle updating an object"""
        return Response({'method':'PUT'})
    def patch(self, request,pk=None):
        """Handle partial update of object"""
        return Response({'method':"PATCH"})
    def delete(self, request, pk=None):
        """Delete and object"""
        return Response({'method':'DELETE'})



from rest_framework import viewsets
class HelloViewSet(viewsets.ViewSet):
    """Test api viewset"""

    serializer_class=serializers.HelloSerializer
    def list(self, request):
        """Return hellp message"""
        a_view_set=[
            'Uses actions (list, create, retrieve, update, partial_update)',
            "Automatically maps to URLs using Routers",
            "Provides more functionality with less code",
        ]
        return Response({'message':'Hello',
                        'view_set':a_view_set})
    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name=serializer.validated_data.get('name')
            message=f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method':'GET'})
    def update(self, request, pk=None):
        """Update"""
        return Response({'http_method':'PUT'})
    def partial_update(self, request, pk=None):
        """partial update"""
        return Response({'http_method':'PATCH'})
    def destroy(self, request, pk=None):
        """removing"""
        return Response({'http_method':'DELETE'})



from profiles_api import models,permissions
from rest_framework import authentication, filters

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class=serializers.UserProfileSerializer
    queryset= models.UserProfile.objects.all()
    authentication_classes= (authentication.TokenAuthentication,)#Specify the authentication process we use in our API so we can verify who the user is
    permission_classes=(permissions.UpdateOwnProfile,)#Specify the permission level of the authenticated user
    filter_backends=(filters.SearchFilter,)
    search_fields=('name', 'email',)



from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    #make it visible in browsable API, the other viewsets have this by default, but not obtainauthtoken
    renderer_classes= api_settings.DEFAULT_RENDERER_CLASSES

from rest_framework import permissions as rest_permissions

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handling creating, reading and updating profile feeds"""
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class= serializers.ProfileFeedSerializer
    queryset=models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,#only able to update their own
        rest_permissions.IsAuthenticated,#Limit viewing to authenticated user only
        rest_permissions.IsAuthenticatedOrReadOnly#if not logged in, can't edit
    )
    
    def perform_create(self, serializer):#Override behavior for creating objects through a model viewset
        """Sets the user profile to the logged-in user"""
        #because we have added token_authentication, the request contains info on user
        serializer.save(user_profile=self.request.user)#since the serializer is a modelserializer, it has save function to save content from serializer to database