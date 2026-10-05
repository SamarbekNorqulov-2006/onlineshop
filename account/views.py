from django.shortcuts import render
from .models import NEW, CODE_VERIFY, CustomUser, VerifyCode
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from .serializers import SignUpSerializer, VerifySerializer

from rest_framework import permissions, status
from datetime import datetime
from rest_framework.response import Response


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = CustomUser.objects.all()


class VerifyView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VerifySerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        code = request.data.get('code')
        user = request.user

        verify = user.codes.filter(
            code=code,
            used=False,
            expiration_time__gte=datetime.now()
        ).first()

        if verify:
            verify.used = True
            verify.save()
            user.auth_status = CODE_VERIFY  
            user.save()
            return Response({'message': 'Tasdiq muvaffaqiyatli!'}, status=status.HTTP_200_OK)

        return Response({"error": "Kod noto'g'ri yoki muddati o'tgan"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def get(self, request):
        user = request.user
        data = {
            'email': user.email,
            'phone_number': user.phone_number,
            'username': user.username
        }
        return Response(data)


