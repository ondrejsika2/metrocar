__author__="Xaralis"
__date__ ="$28.10.2009 16:22:56$"

from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.create_update import get_model_and_form_class

def list_obj(model, page=1, per_page=30, order_by='pk', all=False, **kwargs):
    res_dict = {
        'page' : 1,
        'count' : 0,
        'num_pages' : 1,
        'page_range' : [1]
    }

    qset = model.objects.all().order_by(order_by)
    if len(kwargs):
            qset = qset.filter(**kwargs)
            
    if all:
        res_dict['object_list'] = qset
        res_dict['page'] = 1
        res_dict['count'] = len(res_dict['object_list'])
    else:
        paginator = Paginator(qset, per_page)
        res_dict['object_list'] = paginator.page(page).object_list
        res_dict['page'] = page
        res_dict['count'] = paginator.count
        res_dict['num_pages'] = paginator.num_pages
        res_dict['page_range'] = paginator.page_range

    return res_dict

def get_obj(model, **kwargs):
    if not len(kwargs):
        return False

    return model.objects.get(**kwargs)

def create_obj(model, data, form_class=None):
    model, form_class = get_model_and_form_class(model, form_class)
    form = form_class(data)
    if form.is_valid():
        new_object = form.save()
        return new_object.id
    else:
        return 0

def update_obj(model, object_id, data, form_class=None):
    model, form_class = get_model_and_form_class(model, form_class)
    obj = get_obj(model, pk__exact=object_id)
    form = form_class(data, instance=obj)
    if form.is_valid():
        obj = form.save()
        return obj.id
    else:
        return 0

def delete_obj(model, object_id):
    obj = get_obj(model, pk__exact=object_id)
    if obj == False:
        return False
    else:
        obj.delete()
        return True

