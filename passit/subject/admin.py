from django.contrib import admin
from django.db import models
from django.db.models import QuerySet
from django.db.models.aggregates import Count
from django.forms import widgets
from django.http import HttpRequest

from passit.subject.models import Subject, SubjectOfAgeGroup, Exam, Resource, FieldOfStudy, FieldOfStudyOfAgeGroup
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
    inlines = [ExamInline, LecturerOfSubjectInlineAdmin]

    def get_queryset(self, request: HttpRequest) -> 'QuerySet[SubjectOfAgeGroup]':
        return super().get_queryset(request).select_related('field_age_group', 'field_age_group__field_of_study')


@admin.register(FieldOfStudyOfAgeGroup)
class FieldOfStudyOfAgeGroupAdmin(admin.ModelAdmin):

    def get_queryset(self, request: HttpRequest) -> 'QuerySet[FieldOfStudyOfAgeGroup]':
        return super().get_queryset(request).select_related('field_of_study')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [ResourceInlineAdmin, ]
    formfield_overrides = {
        models.TextField: {'widget': widgets.Textarea(attrs={'rows': 5, 'cols': 40})},
    }

    def get_queryset(self, request: HttpRequest) -> 'QuerySet[Subject]':
        return super(SubjectAdmin, self).get_queryset(request).select_related('field_of_study').annotate(resource_count=Count("resources"))

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
    list_display = ('subject_group', 'starts_at', 'place')
    search_fields = ('place',)
    list_filter = ('starts_at',)


admin.site.register(SubjectOfAgeGroup, SubjectOfAgeGroupAdmin)
admin.site.register(FieldOfStudy)
