import uuid
import random
import string
from django.db import models
from accounts.models import User


def generate_family_code():
    """6 belgili unikal invite code: ABC123"""
    chars = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choices(chars, k=6))
        if not Family.objects.filter(invite_code=code).exists():
            return code


class Family(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    invite_code = models.CharField(max_length=6, unique=True, editable=False)

    home_latitude = models.FloatField(null=True, blank=True)
    home_longitude = models.FloatField(null=True, blank=True)
    home_address = models.CharField(max_length=255, null=True, blank=True)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_families'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Families'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = generate_family_code()
        super().save(*args, **kwargs)

    @property
    def members_count(self):
        return self.members.filter(is_active=True).count()

    def __str__(self):
        return f'{self.name} [{self.invite_code}]'


class FamilyMember(models.Model):
    class Role(models.TextChoices):
        PARENT = 'parent', 'Ota-ona'
        CHILD = 'child', 'Farzand'

    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_memberships')
    role = models.CharField(max_length=10, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('family', 'user')
        ordering = ['joined_at']

    def __str__(self):
        return f'{self.user.full_name} — {self.family.name} ({self.role})'
