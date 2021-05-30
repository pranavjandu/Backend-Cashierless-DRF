from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','username','password','is_customer','is_guard','is_online')


class CustomRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','username','password','is_customer','is_guard')
        extra_kwargs = {'password': {'write_only': True}}

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password': self.validated_data.get('password', ''),
            'is_customer': self.validated_data.get('is_customer', ''),
            'is_guard': self.validated_data.get('is_guard', ''),
            
        }

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(username, email, password, **validated_data)
        return user


    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.email = self.cleaned_data.get('email')
        user.is_customer = self.cleaned_data.get('is_customer')
        user.is_guard = self.cleaned_data.get('is_guard')
        print("In Save")
        user.save()
        adapter.save_user(request, user, self)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")



        