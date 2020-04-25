from rest_framework import fields, serializers, viewsets, mixins
from rest_framework_gis.fields import GeometryField, GeometrySerializerMethodField

from drf_spectacular.fields import OpenApiSerializerFieldExtension
from drf_spectacular.plumbing import build_basic_type
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.validation import validate_schema
from tests import generate_schema


class Base64Field(fields.Field):
    pass  # pragma: no cover


def test_serializer_field_extension_base64(no_warnings):
    class Base64FieldExtension(OpenApiSerializerFieldExtension):
        target_class = 'tests.test_extensions.Base64Field'

        def map_serializer_field(self, auto_schema):
            return build_basic_type(OpenApiTypes.BYTE)

    class XSerializer(serializers.Serializer):
        hash = Base64Field()

    class XViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
        serializer_class = XSerializer

    schema = generate_schema('x', XViewset)
    validate_schema(schema)
    assert schema['components']['schemas']['X']['properties']['hash']['type'] == 'string'
    assert schema['components']['schemas']['X']['properties']['hash']['format'] == 'byte'


def test_serializer_field_extension_geo(no_warnings):
    class XSerializer(serializers.Serializer):
        location = GeometryField()

    class XViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
        serializer_class = XSerializer

    schema = generate_schema('x', XViewset)
    validate_schema(schema)
    assert isinstance(schema['components']['schemas']['X']['properties']['location'], dict)
    assert len(schema['components']['schemas']['X']['properties']['location']['oneOf']) == 2
    assert schema['components']['schemas']['X']['properties']['location']['oneOf'][0]['type'] == 'object'
    assert schema['components']['schemas']['X']['properties']['location']['oneOf'][0]['required'] == ['type', 'coordinates']
    assert schema['components']['schemas']['X']['properties']['location']['oneOf'][1]['type'] == 'object'
    assert schema['components']['schemas']['X']['properties']['location']['oneOf'][1]['required'] == ['type', 'geometries']


def test_serializer_field_extension_geojson(no_warnings):
    class XSerializer(serializers.Serializer):
        location = GeometrySerializerMethodField()

    class XViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
        serializer_class = XSerializer

    schema = generate_schema('x', XViewset)
    validate_schema(schema)
    assert isinstance(schema['components']['schemas']['X']['properties']['location'], dict)
    assert len(schema['components']['schemas']['X']['properties']['location']['oneOf']) == 2
    assert schema['components']['schemas']['X']['properties']['location']['oneOf'][0]['type'] == 'object'
    assert schema['components']['schemas']['X']['properties']['location']['oneOf'][0]['required'] == ['id', 'type', 'geometry']
    assert schema['components']['schemas']['X']['properties']['location']['oneOf'][1]['type'] == 'object'
    assert schema['components']['schemas']['X']['properties']['location']['oneOf'][1]['required'] == ['id', 'type', 'features']
