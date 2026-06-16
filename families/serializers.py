from rest_framework import serializers
from .models import Family, FamilyMember
from accounts.models import User


class MemberUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'role', 'avatar')


class FamilyMemberSerializer(serializers.ModelSerializer):
    user = MemberUserSerializer(read_only=True)

    class Meta:
        model = FamilyMember
        fields = ('id', 'user', 'role', 'joined_at')


class FamilySerializer(serializers.ModelSerializer):
    members = FamilyMemberSerializer(many=True, read_only=True)
    members_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Family
        fields = (
            'id', 'name', 'invite_code',
            'home_latitude', 'home_longitude', 'home_address',
            'members_count', 'members', 'created_at',
        )
        read_only_fields = ('id', 'invite_code', 'created_at')


class CreateFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ('name', 'home_latitude', 'home_longitude', 'home_address')

    def create(self, validated_data):
        user = self.context['request'].user
        family = Family.objects.create(created_by=user, **validated_data)
        # Yaratuvchini parent sifatida qo'shamiz
        FamilyMember.objects.create(family=family, user=user, role=FamilyMember.Role.PARENT)
        return family

    def to_representation(self, instance):
        return FamilySerializer(instance, context=self.context).data


class JoinFamilySerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6, min_length=6)
    display_name = serializers.CharField(max_length=100, required=False, help_text="Farzand ismi (ixtiyoriy)")

    def validate_invite_code(self, value):
        value = value.upper()
        try:
            self.family = Family.objects.get(invite_code=value)
        except Family.DoesNotExist:
            raise serializers.ValidationError('Kod noto\'g\'ri yoki muddati o\'tgan.')
        return value

    def validate(self, data):
        user = self.context['request'].user
        if FamilyMember.objects.filter(family=self.family, user=user).exists():
            raise serializers.ValidationError('Siz allaqachon bu oilaga a\'zo siz.')
        return data

    def save(self):
        user = self.context['request'].user
        display_name = self.validated_data.get('display_name')

        if display_name:
            user.full_name = display_name
            user.save(update_fields=['full_name'])

        member = FamilyMember.objects.create(
            family=self.family,
            user=user,
            role=FamilyMember.Role.CHILD,
        )
        return member
