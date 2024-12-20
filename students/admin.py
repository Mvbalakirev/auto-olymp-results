from django.contrib import admin

from .models import Group, Student


@admin.action(description="Сбросить класс")
def reset_group(modeladmin, request, queryset):
    queryset.update(group=None)

class StudentAdmin(admin.ModelAdmin):
    fields = ['last_name', 'first_name', 'middle_name', 'group', 'date_of_birth']
    list_display = ('last_name', 'first_name', 'middle_name', 'group', 'date_of_birth')
    search_fields = ['last_name', 'first_name', 'middle_name']
    list_filter = ['group__num', 'group__liter']
    actions = [reset_group]


@admin.action(description="Перевести на следующий год")
def to_next_year(modeladmin, request, queryset):
    for group in queryset:
        group.num += 1
        group.save()

@admin.action(description="Перевести на предыдущий год")
def to_prev_year(modeladmin, request, queryset):
    for group in queryset:
        group.num -= 1
        group.save()

class GroupAdmin(admin.ModelAdmin):
    search_fields = ['num', 'liter']
    actions = [to_next_year, to_prev_year]
    

admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)