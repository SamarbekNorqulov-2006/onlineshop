from django.shortcuts import render
from .models import NEW, CODE_VERIFY, CustomUser
from rest_framework.generics import CreateAPIView,GenericAPIView
from .serializers import SignUpSerializers
from rest_framework import permissions
from datetime import datetime



class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializers
    queryset = CustomUser.objects.all()

class VerifyVeiw(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request):
        code = request.data.get('code')
        user = request.user

        codes = user.code.all().filter(code=code, used=False, expiration_time_gte = datetime.now()).first()


