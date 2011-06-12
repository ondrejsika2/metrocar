__author__ = "Xaralis"
__date__ = "$28.10.2009 17:35:10$"

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from metrocar.user_management.models import *
from metrocar.user_management.models import Account
from metrocar.user_management.models import Company
from metrocar.user_management.models import Deposit
from metrocar.user_management.models import MetrocarUser
from metrocar.user_management.models import UserCard
from metrocar.user_management.models import UserRegistrationRequest
from metrocar.utils.permissions import PermissionsNameConst as PermName
from metrocar.user_management.forms import MetrocarUserCreationForm,MetrocarUserChangeForm


class MetrocarUserCreationForm(UserCreationForm):
    class Meta:
        model = MetrocarUser
        fields = ('username', )

class MetrocarUserChangeForm(UserChangeForm):
    class Meta:
        model = MetrocarUser


class MetrocarUserAdmin(UserAdmin):

    fieldsets = (
                 (None, {'fields': ('username', 'password')}),
                 (_('Personal info'), {'fields': ('first_name', 'last_name', 'gender', 'date_of_birth', 'identity_card_number', 'drivers_licence_number', 'home_subsidiary','language')}),
                 (_('Contacts'), {'fields': ('email', 'primary_phone', 'secondary_phone')}),
                 (_('Important dates'), {'fields': ('last_login', 'date_joined', 'invoice_date')}),
                 (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
                 (_('Groups'), {'fields': ('groups',)}),
                 )
    user_fieldsets = (
                      (None, {'fields': ('username', 'password')}),
                      (_('Personal info'), {'fields': ('first_name', 'last_name', 'gender', 'date_of_birth', 'identity_card_number', 'drivers_licence_number')}),
                      (_('Contacts'), {'fields': ('email', 'primary_phone', 'secondary_phone')}),
                      (_('Important dates'), {'fields': ('last_login', 'date_joined', 'invoice_date')}),
                      )

    list_display = ('username', 'email', 'first_name', 'last_name', 'home_subsidiary', 'invoice_date', 'variable_symbol')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'home_subsidiary')
    form = MetrocarUserChangeForm
    add_form = MetrocarUserCreationForm

    def get_fieldsets(self, request, obj=None):
        """
        Overloaded get_fieldset to prevent permissions escalation for normal users
        Only superuser is able to change admin rights, so we check for it and act show him extended choises
        """
        if(request.user.is_superuser == False):
            self.fieldsets = self.user_fieldsets
        
        return super(MetrocarUserAdmin, self).get_fieldsets(request, obj)

    def has_delete_permission(self, request, obj=None):
        has_perm = super(MetrocarUserAdmin, self).has_delete_permission(request, obj)
        if(obj != None):
            subsidiary = obj.home_subsidiary.name
            perm = self.opts.app_label + "." + PermName.can_delete_user_sub + subsidiary
            has_perm = (has_perm and request.user.has_perm(perm))

        return has_perm

    def save_model(self, request, obj, form, change):
        """
        subsidiary = obj.home_subsidiary.name

        if(change == True):
            perm = self.opts.app_label + "." + PermName.can_change_user_sub + subsidiary
        else:
            perm = self.opts.app_label + "." + PermName.can_add_user_sub + subsidiary

        if(request.user.has_perm(perm) == False):
            raise PermissionDenied
        """

        super(MetrocarUserAdmin, self).save_model(request, obj, form, change)

class UserRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'approved')
    fieldsets = (
                 (None, {'fields': ()}),
                 )

    def set_approved(self, request, queryset):
        for req in queryset:
            print 'expelliarmus'
            if(self.check_approve_permission(request, req) == False):
                raise PermissionDenied
            req.approve()
    set_approved.short_description = _("Mark selected stories as approved")

    def set_denied(self, request, queryset):
        for req in queryset:
            if(self.check_deny_permission(request, req) == False):
                raise PermissionDenied
            req.reject()
    set_denied.short_description = _("Mark selected stories as denied")

    def check_approve_permission(self, request, obj=None):
        if(obj == None):
            return True
        subsidiary = unicode(obj.user.home_subsidiary)
        perm = self.opts.app_label + "." + PermName.can_approve_reg_req_sub + subsidiary
#        print perm
        return request.user.has_perm(perm)

    def check_deny_permission(self, request, obj=None):
        if(obj == None):
            return True
        subsidiary = unicode(obj.user.home_subsidiary)
        perm = self.opts.app_label + "." + PermName.can_deny_reg_req_sub + subsidiary
#        print perm
        return request.user.has_perm(perm)

    def has_change_permission(self, request, obj=None):
        return (self.check_deny_permission(request, obj) or
                self.check_approve_permission(request, obj) or
                super(UserRegistrationRequestAdmin, self).has_change_permission(request, obj))

    actions = [set_approved, set_denied]


admin.site.register(MetrocarUser, MetrocarUserAdmin)
admin.site.unregister(User)
admin.site.register(Company)
admin.site.register(Account)
admin.site.register(UserCard)
admin.site.register(Deposit)
admin.site.register(UserRegistrationRequest,UserRegistrationRequestAdmin)
