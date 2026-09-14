from rest_framework import serializers
from ...models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({'detail':'passwords dosnt match!'})
    
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return super().validate(attrs)
    
    def create(self, validated_date):
        validated_date.pop('confirm_password', None)
        return User.objects.create_user(**validated_date)