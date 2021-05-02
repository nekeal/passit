from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from accounts.models import User
from .models import CustomUser, Membership, UserProfile


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    inlines = [
        MembershipInline,
    ]


class UserProfileInline(admin.TabularInline):
    model = UserProfile


class CustomUserAdmin(UserAdmin):
    inlines = [
        UserProfileInline,
    ]


admin.site.register(CustomUser, CustomUserAdmin)
