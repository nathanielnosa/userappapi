from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt

from . models import Profile
from . serializers import UserSerializer,ProfileSerializer,RegistrationSerializer, UpdateProfileSerializer


# Register View.
class Register(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Login view
class Login(APIView):
    @csrf_exempt
    def post(self,request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(username=username, password=password)
            print(f'::::::::{request.data}')
            if user is not None:
                login(request,user)
                return Response({"Message":"Login successful"},status=status.HTTP_200_OK)
            return Response({"Message":"Login failed"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Logout view
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    @csrf_exempt
    def post(self,request):
        try:
            logout(request)
            return Response({"Message":"Logout successful"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Dashboard View
class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.profile
            return Response({'profile': profile.fullname}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# Update View
class UpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.profile 
            serializer = UpdateProfileSerializer(profile)  # Serialize profile data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def put(self, request):
        try:
            profile = request.user.profile  
            serializer = UpdateProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
