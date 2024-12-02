from django.contrib import admin

from .models import Olymp, OlympStage, OlympStageSubject, Subject


class OlympStageInline(admin.TabularInline):
    model = OlympStage
    extra = 0

class OlympAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'year']}),
    ]
    inlines = [OlympStageInline]

class OlympStageSubjectInline(admin.TabularInline):
    model = OlympStageSubject
    extra = 0

class OlympStageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'olymp')
    search_fields = ('olymp__name', 'name', 'year')
    fieldsets = [
        (None, {'fields': ['name', 'num']}),
    ]
    inlines = [OlympStageSubjectInline]


admin.site.register(Subject)
admin.site.register(Olymp, OlympAdmin)
admin.site.register(OlympStage, OlympStageAdmin)
admin.site.register(OlympStageSubject)