from django.contrib import admin
from .models import User
# Register your models here.
from .models import User, BookmarkedLink


@admin.register(BookmarkedLink)
class BookmarkedLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'link', 'status', 'created_at']
    list_display_links = ['id', 'user', 'link']
    readonly_fields = ['created_at']


class BookmarkedLinkTabularInline(admin.TabularInline):
    model = BookmarkedLink
    fields = ['id', 'link', 'status', 'created_at']
    readonly_fields = ['id', 'created_at']
    extra = 0



class UserAdmin(admin.ModelAdmin):
    # fields = ['first_name', 'last_name', 'is_staff', 'password']
    fieldsets = (
        ('Personal Information', {
            "fields": (
                ('first_name', 'last_name'),
            ),
        }),
        ('Credentials', {
            "fields": (
                'email', 'password'
            ),
        }),
        ('Permissions', {
            "fields": (
                'is_staff', 'is_superuser'
            ),
            'classes': ('collapse',),
        }),
    )
    
    # list_display = ['id', 'first_name', 'last_name']
    # list_editable = ['last_name']
    # list_display_links = ['first_name']
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_superuser']
    # list_editable = ['last_name']
    list_display_links = ['id', 'email',]
    readonly_fields = ['password']
    inlines = [
        BookmarkedLinkTabularInline
    ]
    readonly_fields = ['password']


admin.site.register(User, UserAdmin)
