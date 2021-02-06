from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from accounts.forms import UsercreationForm, UserchangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
User=get_user_model()
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    add_form = UsercreationForm
    form=UserchangeForm
    list_display = ('id','email','first_name','last_name','is_active','is_staff','is_superuser','is_varified' )
    # readonly_fields = ('email',)
    list_filter = ('is_superuser',)
    list_display_links = ('email','id')
    list_per_page = 4
    fieldsets = (
        (

            None, {'fields': ('email','first_name','last_name','password',)}
        ),
        (
            'Permissions',{
                'fields':('is_superuser','is_staff','is_active','is_varified')
            }
        )
    )
    add_fieldsets = (
        (

            None,{
                'classes': ('wide',),
                'fields': ('email','first_name','last_name','password1','password2','is_active')
            }
        ),
        ('permissions',{'fields' : ('is_superuser','is_staff','is_active','is_varified')}
         )
    )
    ordering = ('id',)
    search_fields = ('email',)
    filter_horizontal = ()

admin.site.register(User,UserAdmin)