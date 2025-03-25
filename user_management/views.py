from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializer import RegisterSerializer, UserSerializer
from .permissions import IsOwnerOrAdmin

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),

    }

# Create your views here.
class Register(APIView):
    
    def post(self, request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    def post(self, request):
        email= request.data.get('email')
        password=request.data.get('password')

        if not email:
            return Response({'message':"Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not password:
            return Response({'message':"Password is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user=User.objects.filter(email=email).first()
        if user is None:
            return Response({'message':"Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            return Response({'message':'Invalid password!'}, status=status.HTTP_401_UNAUTHORIZED)
        token= get_tokens_for_user(user)
        return Response({'message':'Login successful!', 'token': token}, status=status.HTTP_202_ACCEPTED)


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class ProfileDetail(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def put(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)