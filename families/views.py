from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Family, FamilyMember
from .serializers import (
    CreateFamilySerializer,
    FamilySerializer,
    JoinFamilySerializer,
)


class CreateFamilyView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Oila yaratish",
        description="Faqat parent role uchun. Oila yaratib, invite code generatsiya qiladi.",
        request=CreateFamilySerializer,
        responses={201: FamilySerializer},
        tags=["Family"],
    )
    def post(self, request):
        if request.user.role != 'parent':
            return Response(
                {'detail': 'Faqat ota-ona oila yarata oladi.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = CreateFamilySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        family = serializer.save()
        return Response(serializer.to_representation(family), status=status.HTTP_201_CREATED)


class MyFamiliesView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Mening oilalarim",
        description="Foydalanuvchi a'zo bo'lgan barcha oilalar.",
        responses={200: FamilySerializer(many=True)},
        tags=["Family"],
    )
    def get(self, request):
        family_ids = FamilyMember.objects.filter(
            user=request.user, is_active=True
        ).values_list('family_id', flat=True)

        families = Family.objects.filter(id__in=family_ids)
        serializer = FamilySerializer(families, many=True, context={'request': request})
        return Response(serializer.data)


class FamilyDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, family_id, user):
        try:
            family = Family.objects.get(id=family_id)
            FamilyMember.objects.get(family=family, user=user, is_active=True)
            return family
        except (Family.DoesNotExist, FamilyMember.DoesNotExist):
            return None

    @extend_schema(
        summary="Oila ma'lumotlari",
        description="Oila haqida to'liq ma'lumot va barcha a'zolar.",
        responses={200: FamilySerializer},
        tags=["Family"],
    )
    def get(self, request, family_id):
        family = self.get_object(family_id, request.user)
        if not family:
            return Response({'detail': 'Topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FamilySerializer(family, context={'request': request})
        return Response(serializer.data)


class JoinFamilyView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Oilaga qo'shilish",
        description="Invite code orqali oilaga child sifatida qo'shilish.",
        request=JoinFamilySerializer,
        responses={200: FamilySerializer},
        tags=["Family"],
    )
    def post(self, request):
        serializer = JoinFamilySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        family_data = FamilySerializer(member.family, context={'request': request}).data
        return Response(family_data, status=status.HTTP_200_OK)


class FamilyMembersView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Oila a'zolari",
        description="Oiladagi barcha aktiv a'zolar ro'yxati.",
        responses={200: OpenApiResponse(description="A'zolar ro'yxati")},
        tags=["Family"],
    )
    def get(self, request, family_id):
        # Foydalanuvchi bu oilaga a'zo ekanligini tekshirish
        if not FamilyMember.objects.filter(
            family_id=family_id, user=request.user, is_active=True
        ).exists():
            return Response({'detail': 'Ruxsat yo\'q.'}, status=status.HTTP_403_FORBIDDEN)

        members = FamilyMember.objects.filter(
            family_id=family_id, is_active=True
        ).select_related('user')

        from .serializers import FamilyMemberSerializer
        serializer = FamilyMemberSerializer(members, many=True)
        return Response(serializer.data)
