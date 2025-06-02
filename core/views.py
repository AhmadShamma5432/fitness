from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.mixins import * 
from rest_framework.viewsets import GenericViewSet
from .models import User,Profile
from .serializers import UserRetrieveSerializer,UserUpdateSerializer,ProfileSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserUpdateView(RetrieveModelMixin,UpdateModelMixin,ListModelMixin,GenericViewSet):

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UserUpdateSerializer
        else:
            return UserRetrieveSerializer
        
class ProfileView(
    CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet
):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user_id=self.request.user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = self.perform_create(serializer)
        return Response(ProfileSerializer(profile).data)


