from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response#Return response object from API view

# Create your views here.

class HelloAPIView(APIView):
    """Test APIView"""

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
