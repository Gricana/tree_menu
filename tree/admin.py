from django.contrib import admin
from .models import Menu, MenuItem


class MenuItemInline(admin.StackedInline):
    model = MenuItem
    extra = 1


class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]
    list_display = ('name',)
    prepopulated_fields = {"name": ("name",)}


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'url', 'named_url')
    search_fields = ('title', 'named_url')
    list_filter = ('menu', 'parent')
    list_editable = ('url', 'named_url',)


admin.site.site_header = "Tree Menu | UpTrade Test"
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
