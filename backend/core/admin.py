from django.contrib import admin

from .models import Owner, Guest, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'password', 'first_access', 'chat_id')
    inlines = [PhotoInline]

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'nickname', 'relationship', 'owner')
    readonly_fields = ('owner',)
    inlines = [PhotoInline]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('file', 'slug', 'guest')