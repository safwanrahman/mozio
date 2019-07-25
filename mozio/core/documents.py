from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.documents import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import query

from .models import ServiceArea


@registry.register_document
class ServiceAreaDocument(Document):
    area = fields.GeoShapeField()
    created_by = fields.KeywordField()

    class Index:
        name = 'service_area'

    class Django:
        model = ServiceArea
        fields = ["id", "name", "price"]

    def prepare_created_by(self, instance):
        return str(instance.created_by)

    @classmethod
    def get_inside_query(cls, lat, lon):
        return query.GeoShape(area={"shape": {"type": "Point", "coordinates": [lon, lat]}})
