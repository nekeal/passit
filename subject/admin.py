from typing import Any

from django.contrib import admin
from django.forms import widgets
from django.db import models

from common.admin import OwnedModelAdminMixin
from lecturers.models import LecturerOfSubject
from subject.models import Subject, SubjectOfAgeGroup, Exam, Resource, FieldOfStudies


class ExamInline(admin.TabularInline):
    model = Exam
    extra = 1


class LecturerOfSubjectInlineAdmin(admin.TabularInline):
    model = LecturerOfSubject
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


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [ResourceInlineAdmin, ]
    formfield_overrides = {
        models.TextField: {'widget': widgets.Textarea(attrs={'rows': 5, 'cols': 40})},
    }

    def save_formset(self, request, form, formset, change):
        if formset.model == Resource:
            instances = formset.save(commit=False)
            for instance in instances:
                if not instance.pk:
                    instance.created_by = request.user
                instance.modified_by = request.user
                instance.save()
        super(SubjectAdmin, self).save_formset(request, form, formset, change)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject_group', 'starts_at', 'place')
    search_fields = ('place',)
    list_filter = ('starts_at',)


admin.site.register(SubjectOfAgeGroup, SubjectOfAgeGroupAdmin)
admin.site.register(FieldOfStudies)
