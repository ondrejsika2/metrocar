from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

from metrocar.utils.permissions import create_or_get_custom_permission
from metrocar.utils.permissions import PermissionsNameConst as PermName


class SubsidiaryManager(models.Manager):
    def get_current(self):
        site = Site.objects.get_current()
        return self.get(site=site)


class Subsidiary(models.Model):
    """
    Represents company subsidiary. Implementation is based on django Site object
    with some extended data.
    """
    name = models.CharField(_('Name'), max_length=255)
    email = models.EmailField(_('E-mail'))
    street = models.CharField(_('Street'), max_length=100)
    house_number = models.IntegerField(_('House number'), max_length=8)
    city = models.CharField(_('City'), max_length=80)
    tax_rate = models.FloatField(_('Tax rate'), default=21)

    site = models.OneToOneField(Site)

    use_onboard_unit = models.BooleanField(_('Use onboard unit in cars'),
        default=True)

    objects = SubsidiaryManager()

    class Meta:
        verbose_name = _('Subsidiary')
        verbose_name_plural = _('Subsidiaries')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "http://%s" % self.site.domain

    @property
    def url(self):
        return self.get_absolute_url()

    def save(self, **kwargs):
        """
        Creates new subsidiary and  new set of permissions for action bounded to it
        """
        super(Subsidiary, self).save(**kwargs)

        #create new set of permissions
        create_or_get_custom_permission("UserRegistrationRequest",
                                        "Can deny registration request " + self.name,
                                        PermName.can_deny_reg_req_sub + self.name)
        create_or_get_custom_permission("UserRegistrationRequest",
                                        "Can approve registration request " + self.name,
                                        PermName.can_approve_reg_req_sub + self.name)
        create_or_get_custom_permission("Car",
                                        "Can add car to subsidiary " + self.name,
                                        PermName.can_add_car_sub + self.name)
        create_or_get_custom_permission("Car",
                                        "Can change car in subsidiary " + self.name,
                                        PermName.can_change_car_sub + self.name)
        create_or_get_custom_permission("Car",
                                        "Can delete car in subsidiary " + self.name,
                                        PermName.can_delete_car_sub + self.name)
        create_or_get_custom_permission("MetrocarUser",
                                        "Can add user in subsidiary " + self.name,
                                        PermName.can_add_user_sub + self.name)
        create_or_get_custom_permission("MetrocarUser",
                                        "Can change user in subsidiary " + self.name,
                                        PermName.can_change_user_sub + self.name)
        create_or_get_custom_permission("MetrocarUser",
                                        "Can delete user in subsidiary " + self.name,
                                        PermName.can_delete_user_sub + self.name)

    def delete(self):
        """
        Deletes subsidiary and its associated permissions
        """
        super(Subsidiary, self).delete()

        #delete permissions
        create_or_get_custom_permission("UserRegistrationRequest",
                                        "Can deny registration request " + self.name,
                                        PermName.can_deny_reg_req_sub + self.name).delete()
        create_or_get_custom_permission("UserRegistrationRequest",
                                        "Can approve registration request " + self.name,
                                        PermName.can_approve_reg_req_sub + self.name).delete()
        create_or_get_custom_permission("Car",
                                        "Can add car to subsidiary " + self.name,
                                        PermName.can_add_car_sub + self.name).delete()
        create_or_get_custom_permission("Car",
                                        "Can change car in subsidiary " + self.name,
                                        PermName.can_change_car_sub + self.name).delete()
        create_or_get_custom_permission("Car",
                                        "Can delete car in subsidiary " + self.name,
                                        PermName.can_delete_car_sub + self.name).delete()
        create_or_get_custom_permission("MetrocarUser",
                                        "Can add user in subsidiary " + self.name,
                                        PermName.can_add_user_sub + self.name).delete()
        create_or_get_custom_permission("MetrocarUser",
                                        "Can change user in subsidiary " + self.name,
                                        PermName.can_change_user_sub + self.name).delete()
        create_or_get_custom_permission("MetrocarUser",
                                        "Can delete user in subsidiary " + self.name,
                                        PermName.can_delete_user_sub + self.name).delete()
