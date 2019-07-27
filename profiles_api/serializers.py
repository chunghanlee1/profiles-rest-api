from rest_framework import serializers

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name= serializers.CharField(max_length=10)





from profiles_api import models

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.UserProfile
        fields=('id','email','name','password')
        extra_kwargs= {
            'password': {
                'write_only':True,
                'style': {'input_type':'password'}
            }
        }
    def create(self, validated_data):#Replace the default create function so password is displayed as a hash instead of clear text
        """Create and return new user"""
        user=models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user
    