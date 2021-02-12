from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django_admin_display import admin_display

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "get_field_of_study",
        "get_students_start_year",
        "get_subject",
    ]

    def get_queryset(self, request: HttpRequest) -> "QuerySet[News]":
        return (
            super()
            .get_queryset(request=request)
            .select_related("field_age_group__field_of_study", "subject_group__subject")
        )

    @admin_display(
        short_description="Field of study",
        admin_order_field="field_age_group__field_of_study",
    )
    def get_field_of_study(self, obj: News):
        if obj.field_age_group:
            return obj.field_age_group.field_of_study

    @admin_display(
        short_description="Subject", admin_order_field="subject_group__subject"
    )
    def get_subject(self, obj: News):
        if obj.subject_group:
            return obj.subject_group.subject

    @admin_display(
        short_description="Students start year",
        admin_order_field="field_age_group__students_start_year",
    )
    def get_students_start_year(self, obj: News):
        if obj.field_age_group:
            return obj.field_age_group.students_start_year
