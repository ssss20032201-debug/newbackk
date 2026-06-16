from django.urls import path
from .views import (
    CreateFamilyView,
    MyFamiliesView,
    FamilyDetailView,
    JoinFamilyView,
    FamilyMembersView,
)

urlpatterns = [
    path('', MyFamiliesView.as_view(), name='family-list'),
    path('create/', CreateFamilyView.as_view(), name='family-create'),
    path('join/', JoinFamilyView.as_view(), name='family-join'),
    path('<uuid:family_id>/', FamilyDetailView.as_view(), name='family-detail'),
    path('<uuid:family_id>/members/', FamilyMembersView.as_view(), name='family-members'),
]
