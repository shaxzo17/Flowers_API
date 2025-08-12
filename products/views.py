from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Flower
from .serializers import RegisterSerializer, LoginSerializer, FlowerSerializer, ProfileSerializer


class RegisterApi(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Foydalanuvchi yaratildi',
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApi(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        }, status=status.HTTP_200_OK)



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Chiqish muvaffaqiyatli!"}, status=status.HTTP_200_OK)


class FlowerListCreateView(generics.ListCreateAPIView):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer


class FlowerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer


class ProfileApi (APIView):
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response ({
        'data': serializer.data,
        'status': status.HTTP_200_OK
        })