from django.contrib import admin
from .models import Family, FamilyMember


class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember
    extra = 0
    readonly_fields = ('joined_at',)


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'invite_code', 'created_by', 'members_count', 'created_at')
    search_fields = ('name', 'invite_code')
    readonly_fields = ('invite_code', 'created_at')
    inlines = (FamilyMemberInline,)


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'family', 'role', 'is_active', 'joined_at')
    list_filter = ('role', 'is_active')
