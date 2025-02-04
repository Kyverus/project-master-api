from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

from .serializers import UserRegistrationSerializer

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True, samesite="None", secure=True )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    
class MyTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get("refresh_token")
        print("DEBUG PRINT", self.context['request'].COOKIES)
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')

class MyTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        print("finalize:",request.COOKIES)
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh_token'],max_age=cookie_max_age, httponly=True, samesite="None", secure=True )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = MyTokenRefreshSerializer

@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    try:
        refresh_token = request.COOKIES.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()
        response = Response({'Logout':'Successfullly'})
        response.delete_cookie('refresh_token')
        return response
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)