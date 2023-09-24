from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'title', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        member = User.objects.create_user(
            title=validated_data['title'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
        )
        member.set_password(validated_data['password'])
        member.save()
        return member


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id
        token['title'] = user.title
        token['email'] = user.email
        return token

