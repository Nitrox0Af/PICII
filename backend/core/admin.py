from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreateForm, CustomUserChangeForm
from .models import Guest, Photo, Access, CustomUser


@admin.register(CustomUser)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUserCreateForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('first_name', 'last_name', 'email', 'first_access', 'chat_id')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'first_access', 'chat_id')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'nickname', 'relationship', 'owner')
    exclude = ['owner',]
    inlines = [PhotoInline]

    def owner(self, obj):
        return str(obj.owner.get_full_name())
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('file', 'slug', 'guest')

@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    list_display = ('date', 'hour', 'guest')
    readonly_fields = ('date', 'hour', 'guest')