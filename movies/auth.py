from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for token pair authentication.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token if needed
        token['user_id'] = str(user.id)
        token['username'] = user.username
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        # Include user_id in the response data
        data['user_id'] = str(self.user.user_id)
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for token pair authentication.
    """
    serializer_class = CustomTokenObtainPairSerializer