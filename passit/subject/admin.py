from django.contrib import admin
from django.db import models
from django.db.models import QuerySet
from django.db.models.aggregates import Count
from django.forms import widgets
from django.http import HttpRequest
from django_admin_display import admin_display

from passit.subject.models import (
    Exam,
    FieldOfStudy,
    FieldOfStudyOfAgeGroup,
    Resource,
    Subject,
    SubjectOfAgeGroup,
)
from ..lecturers.models import LecturerOfSubjectOfAgeGroup


class ExamInline(admin.TabularInline):
    model = Exam
    extra = 1


class LecturerOfSubjectInlineAdmin(admin.TabularInline):
    model = LecturerOfSubjectOfAgeGroup
    extra = 1


class ResourceInlineAdmin(admin.StackedInline):
    model = Resource
    readonly_fields = ['created_by', 'modified_by']
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': widgets.Textarea(attrs={'rows': 5, 'cols': 40})},
    }


class SubjectOfAgeGroupAdmin(admin.ModelAdmin):
    list_display = ["subject", "students_start_year"]
    inlines = [ExamInline, LecturerOfSubjectInlineAdmin]

    def get_queryset(self, request: HttpRequest) -> 'QuerySet[SubjectOfAgeGroup]':
        return (
            super()
            .get_queryset(request)
            .select_related(
                'subject', 'field_age_group', 'field_age_group__field_of_study'
            )
        )


@admin.register(FieldOfStudyOfAgeGroup)
class FieldOfStudyOfAgeGroupAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest) -> 'QuerySet[FieldOfStudyOfAgeGroup]':
        return super().get_queryset(request).select_related('field_of_study')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [
        ResourceInlineAdmin,
    ]
    formfield_overrides = {
        models.TextField: {'widget': widgets.Textarea(attrs={'rows': 5, 'cols': 40})},
    }

    def get_queryset(self, request: HttpRequest) -> 'QuerySet[Subject]':
        return (
            super(SubjectAdmin, self)
            .get_queryset(request)
            .select_related('field_of_study')
            .annotate(resource_count=Count("resources"))
        )

    def save_formset(self, request: HttpRequest, form, formset, change):
        if formset.model == Resource:
            instances = formset.save(commit=False)
            for instance in instances:
                if not instance.pk:
                    instance.created_by = request.user.profile
                instance.modified_by = request.user.profile
                instance.save()
        super(SubjectAdmin, self).save_formset(request, form, formset, change)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('get_field_of_study', 'get_subject', 'starts_at', 'place')
    search_fields = ('place',)
    list_filter = ('starts_at',)

    def get_queryset(self, request: HttpRequest) -> "QuerySet[Exam]":
        return (
            super()
            .get_queryset(request=request)
            .select_related(
                "subject_group__subject",
                "subject_group__field_age_group__field_of_study",
            )
        )

    @admin_display(
        short_description="Field of study",
        admin_order_field="subject_group__field_age_group__field_of_study",
    )
    def get_field_of_study(self, obj: Exam):
        return obj.subject_group.field_age_group.field_of_study

    @admin_display(
        short_description="Subject", admin_order_field="subject_group__subject"
    )
    def get_subject(self, obj: Exam):
        return obj.subject_group.subject


admin.site.register(SubjectOfAgeGroup, SubjectOfAgeGroupAdmin)
admin.site.register(FieldOfStudy)
