'''
Created on 6.12.2010

@author: svehlja3
'''
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from metrocar.utils.log import get_logger

class PermissionsNameConst:
    """
    Simple class for centralizing permission string bases.
    For specifiing simply concate string with + ie.:

        can_deny_reg_req_sub + "SubsidiaryName" will create requested "REG_REQ_DNY_SubsidiaryName"
    """
    can_deny_reg_req_sub = "REG_REQ_DNY_"
    can_approve_reg_req_sub = "REG_REQ_APP_"
    can_add_car_sub = "ADD_CAR_"
    can_change_car_sub = "CHNG_CAR_"
    can_delete_car_sub = "DELETE_CAR_"
    can_add_user_sub = "ADD_USER_"
    can_change_user_sub = "CHNG_USER_"
    can_delete_user_sub = "DELETE_USER_"

def create_or_get_custom_permission(modelname, name, codename):
    modelname = modelname.lower()
    ct = ContentType.objects.get(model=modelname)
    perm, created = Permission.objects.get_or_create(
        codename=codename,
        content_type__pk=ct.id,
        defaults={
            'name': name[:50],  # permission name can be at most 50 chars long!
            'content_type': ct,
        })
    if(created == True):
        get_logger().info("Created new permission: " + unicode(perm))
    return perm

