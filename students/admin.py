from django.contrib import admin

from .models import Group, Student


@admin.action(description="Reset group")
def reset_group(modeladmin, request, queryset):
    queryset.update(group=None)


class StudentAdmin(admin.ModelAdmin):
    fields = ['last_name', 'first_name', 'middle_name', 'group', 'date_of_birth']
    list_display = ('last_name', 'first_name', 'middle_name', 'group', 'date_of_birth')
    search_fields = ['last_name', 'first_name', 'middle_name', 'date_of_birth']
    actions = [reset_group]
    

admin.site.register(Group)
admin.site.register(Student, StudentAdmin)