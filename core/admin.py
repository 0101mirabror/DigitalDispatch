from django.contrib import admin
from core.models import (
    CompanyType,
    Section,
    LinkType,
    GeneralLink,
    Tag,
    Company
)

class CustomModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'author', 'created_time')


@admin.register(GeneralLink)
class GeneralLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'type', 'author', 'created_time')


admin.site.register(Section, CustomModelAdmin)
admin.site.register(LinkType, CustomModelAdmin)
admin.site.register(Tag, CustomModelAdmin)
admin.site.register(CompanyType, CustomModelAdmin)