from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Ro'yxatdan o'tish",
        description="Yangi foydalanuvchi (parent yoki child) yaratish. JWT tokenlar qaytaradi.",
        request=RegisterSerializer,
        responses={201: OpenApiResponse(description="Muvaffaqiyatli ro'yxatdan o'tildi, JWT qaytarildi")},
        tags=["Auth"],
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(serializer.to_representation(instance), status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Kirish",
        description="Email va parol bilan kirish. JWT access + refresh token qaytaradi.",
        request=LoginSerializer,
        responses={200: OpenApiResponse(description="JWT tokenlar qaytarildi")},
        tags=["Auth"],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Parol tiklash — kod yuborish",
        description="Emailga 6 raqamli OTP kod yuboradi. Kod 10 daqiqa amal qiladi.",
        request=PasswordResetRequestSerializer,
        responses={200: OpenApiResponse(description="Kod yuborildi (yoki foydalanuvchi topilmasa ham xuddi shu javob)")},
        tags=["Auth"],
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': "Agar bu email ro'yxatdan o'tgan bo'lsa, kod yuborildi."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Parol tiklash — kodni tasdiqlash",
        description="OTP kodni tekshirib yangi parol o'rnatadi.",
        request=PasswordResetConfirmSerializer,
        responses={200: OpenApiResponse(description="Parol muvaffaqiyatli yangilandi")},
        tags=["Auth"],
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Parol muvaffaqiyatli yangilandi.'}, status=status.HTTP_200_OK)
