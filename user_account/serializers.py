from django.forms import ValidationError
from rest_framework import serializers

from .models import CustomUser

class UserRegisterSerializer(serializers.ModelSerializer):
    password         = serializers.CharField(write_only=True,style={'input_type':'password'})
    confirm_password = serializers.CharField(write_only=True,style={'input_type':'password'})
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','user_role','email','phone_number','address_line_1','address_line_2','city','state','country','password','confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
    
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Password must macth')
        return attrs
    
    def create(self,validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user
           