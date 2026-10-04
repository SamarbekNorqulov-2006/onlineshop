from rest_framework import serializers
from .models import CustomUser, VIA_EMAIL, VIA_PHONE
from base.utils import email_phone_regex
from rest_framework.exceptions import ValidationError
import re
class SignUpSerializers(serializers.ModelSerializer):
    email_or_phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['auth_type', 'auth_status', 'email_or_phone_number','username', 'email', 'phone_number', 'password']

    
    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.save()
        if user.auth == VIA_EMAIL:
            code = user.generate_code(user.auth_type)
            print(f'EMAIL CODE:{code}')

        elif user.auth_type == VIA_PHONE:
            code = user.generate_code(user.auth_type)
            print(f'PHONE NUMBER CODE: {code}')

        else:
            raise ValidationError('Email yoki telifon raqam xato kiritilgan')
        
        return user


    def validate(self, attrs):
        user_input = attrs.get('email_or_phone_number')

        user_input_type = email_phone_regex(user_input)

        if user_input_type == 'email':
            data = {
                'email': user_input,
                'auth_type': VIA_EMAIL
            }
        
        elif user_input == "phone":
            data = {
                "phone_number":user_input,
                "auth_type":VIA_PHONE
            }

        else:
            raise ValidationError("Siz xato email yoki telifon raqam kiritdingiz")
        
        return data
    
    def to_representation(self, instance):
        data = super().to_representation\
        
        return {
            'tokens': instance.token(),
            'data':data
        }
    
    def validate_email(self, value):
        if value and not re.match(EMAIL_REGEX, value):
            raise serializers.ValidationError("Email formati noto'g'ri")
        return value
    

    def validate_phone_number(self, value):
        if value and not re.match(PHONE_REGEX, value):
            raise serializers.ValidationError("Telefon raqami +998XXXXXXXXX formatida bo'lishi kerak")
        return value
    

    def validate_username(self, value):
        if not re.match(USERNAME_REGEX, value):
            raise serializers.ValidationError("Username faqat harf, raqam va '_' dan iborat bo'lishi kerak")
        return value

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_REGEX = r'^\+998[0-9]{9}$'
USERNAME_REGEX = r'^[a-zA-Z0-9_]{3,30}$'