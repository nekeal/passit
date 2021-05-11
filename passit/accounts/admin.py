from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from accounts.models import User
from .models import CustomUser, Membership, UserProfile


class MembershipInline(admin.TabularInline[Membership]):
    model = Membership
    extra = 1


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin[UserProfile]):
    model = UserProfile
    inlines = [
        MembershipInline,
    ]


class UserProfileInline(admin.TabularInline[UserProfile]):
    model = UserProfile


class CustomUserAdmin(UserAdmin):
    inlines = [
        UserProfileInline,
    ]


admin.site.register(CustomUser, CustomUserAdmin)
