# DRIS/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, DisasterReport, AidRequest, Shelter, Volunteer, VolunteerAssignment

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'phone', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone', 'address', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'user_type', 'password1', 'password2'),
        }),
    )

class DisasterReportAdmin(admin.ModelAdmin):
    list_display = ('disaster_type', 'location', 'severity', 'reporter', 'timestamp', 'is_resolved')
    list_filter = ('disaster_type', 'severity', 'is_resolved')
    search_fields = ('location', 'description')
    date_hierarchy = 'timestamp'

class AidRequestAdmin(admin.ModelAdmin):
    list_display = ('aid_type', 'disaster', 'requester', 'timestamp', 'is_fulfilled')
    list_filter = ('aid_type', 'is_fulfilled')
    search_fields = ('description',)
    date_hierarchy = 'timestamp'

class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'current_occupancy')
    search_fields = ('name', 'location')

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'availability')
    list_filter = ('skills', 'availability')
    search_fields = ('user__username', 'certification')

class VolunteerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'aid_request', 'assigned_by', 'assignment_time', 'status')
    list_filter = ('status',)
    search_fields = ('volunteer__user__username', 'aid_request__description')
    date_hierarchy = 'assignment_time'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(DisasterReport, DisasterReportAdmin)
admin.site.register(AidRequest, AidRequestAdmin)
admin.site.register(Shelter, ShelterAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(VolunteerAssignment, VolunteerAssignmentAdmin)