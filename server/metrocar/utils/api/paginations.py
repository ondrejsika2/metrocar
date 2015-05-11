import math
from rest_framework import pagination
from rest_framework import serializers
from metrocar.settings.base import REST_FRAMEWORK

class MetaSerializer(serializers.Serializer):
    next = pagination.NextPageField(source='*')
    prev = pagination.PreviousPageField(source='*')
    count = serializers.Field(source='paginator.count')

    pages = serializers.SerializerMethodField(method_name="get_pages")

    paginate_by = REST_FRAMEWORK['CUSTOM_RECORDS_PER_PAGE']

    def get_pages(self, obj):
        return math.ceil(float(obj.paginator.count) / self.paginate_by)

class CustomPaginationSerializer(pagination.BasePaginationSerializer):
    meta = MetaSerializer(source='*')  # Takes the page object as the source

    results_field = 'results'


class TimelineMetaSerializer(MetaSerializer):
    paginate_by = 5

class TimelinePaginationSerializer(CustomPaginationSerializer):
    meta = TimelineMetaSerializer(source='*')  # Takes the page object as the source

