from django.contrib import admin


class OwnedModelAdminMixin:

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.modified_by = request.user
        print(obj)
        super().save_model(request, obj, form, change)
