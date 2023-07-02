from abc import ABC

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from accounts.models import User


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(write_only=True, )

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name', 'role', 'gender', 'birthdate', 'contact_number', 'img')

    def validate(self, attrs):
        is_email_exist = User.objects.filter(email=attrs["email"]).exists()
        if is_email_exist:
            raise ValidationError("Email is already exist")
        validate_password(attrs['password'])
        return super(SignupSerializer, self).validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super(SignupSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'role', 'gender', 'birthdate', 'contact_number', 'img')

    def update(self, instance, validated_data):
        if 'img' in validated_data:
            instance.img.delete()
            instance.img = validated_data['img']
            validated_data.pop('img', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
