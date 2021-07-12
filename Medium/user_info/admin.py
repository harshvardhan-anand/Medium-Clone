from django.contrib import admin
from .models import LoginHistory, Activity, Profile, Membership, Person
# Register your models here.

# We have not registered Follow model

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'last_login', 'date_joined')
    search_fields = ('username', 'email')

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'country_name', 'device', 'login', 'city')
    list_filter = ('device', 'is_in_european_union')
    date_hierarchy = ('login')
    search_fields = (
        'user', 'country_name', 
        'device', 'longitude', 
        'latitude', 'ip','user_agent',
        'postal_code', 'continent_name',
        'continent_code', 'country_code',
        'city'
    )
    raw_id_fields = ('user', )

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'target','created', 'action_type')
    raw_id_fields = ('user',)
    date_hierarchy = ('created')
    search_fields = ('user', 'action', 'action_type')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership', 'expiry', 'updated')
    raw_id_fields = ('user',)
    date_hierarchy = 'updated'
    search_fields = ('user', 'name', 'email')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'created','expiry')
    date_hierarchy = 'expiry'
    list_filter = ('created',)
    search_fields = ('user',)
    raw_id_fields = ('user',)