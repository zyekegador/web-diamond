from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import (
    UserSerializer, 
    ApplicantRegisterSerializer, 
    HRCreateSerializer,
    LoginSerializer
)

User = get_user_model()


class ApplicantRegisterView(generics.CreateAPIView):
    """Applicants can self-register"""
    queryset = User.objects.all()
    serializer_class = ApplicantRegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Account created successfully'
        }, status=status.HTTP_201_CREATED)


class HRCreateView(generics.CreateAPIView):
    """Only admins can create HR accounts"""
    queryset = User.objects.all()
    serializer_class = HRCreateSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'HR account created successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Login for all user types"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    """Logout - delete token"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CurrentUserView(APIView):
    """Get current logged in user details"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class HRListView(generics.ListAPIView):
    """List all HR staff - Only for admins"""
    queryset = User.objects.filter(user_type='hr')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]