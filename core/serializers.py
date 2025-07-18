from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Debugging statement to check the contents of attrs
        # print(f"Attributes received: {attrs}")

        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        if not credentials['email']:
            raise serializers.ValidationError('email is required')
        if not credentials['password']:
            raise serializers.ValidationError('Password is required')

        user = User.objects.filter(email=credentials['email']).first()
        if user:
            if user.check_password(credentials['password']):
                data = super().validate({
                    'email': user.email,  # Use 'username' key here
                    'password': credentials['password']
                })
                return data
            else:
                raise serializers.ValidationError('Invalid password')
        else:
            raise serializers.ValidationError('User not found')   
              
class UserCreateSerializer(BaseUserCreateSerializer):
    # first_name = serializers.CharField(required=True)
    class Meta(BaseUserCreateSerializer.Meta):
        #the id is auto_field so it doesn't shown in the view of creation
        fields = ['id','email','password','role']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','email','role']

class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','role']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']



class ProfileSerializer(serializers.ModelSerializer):
    weight = serializers.FloatField()
    height = serializers.FloatField()
    goal_weight = serializers.FloatField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "user",
            "weight",
            "goal_weight",
            "height",
            "birth_date",
            "fitness_level",
            "fitness_goal",
            "certification",
            "years_of_experience",
        ]
        read_only_fields = ["id"]

    def get_user(self, obj):
        return obj.user.email

    def create(self, validated_data):
        user_id = self.context['user_id']
        user = User.objects.get(pk=user_id)
        return Profile.objects.create(**validated_data,user=user)
