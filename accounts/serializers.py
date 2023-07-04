from abc import ABC

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from accounts.models import User, PreviousWork, EventPlanner, WorkImages


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


class EventPlannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPlanner
        fields = ['id', 'name', 'email', 'contact_number', 'img']


class WorkImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkImages
        fields = ['id', 'image']


class PreviousWorksSerializer(serializers.ModelSerializer):
    images = WorkImagesSerializer(read_only=True, many=True)
    planner_name = serializers.CharField(source='event_planner.name', read_only=True)
    planner_email = serializers.CharField(source='event_planner.email', read_only=True)
    planner_number = serializers.CharField(source='event_planner.contact_number', read_only=True)

    class Meta:
        model = PreviousWork
        fields = '__all__'
        read_only_fields = ['event_planner']
