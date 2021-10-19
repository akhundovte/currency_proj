
from rest_framework import serializers


class CurrencySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='currency-detail', read_only=True)
    code = serializers.CharField(label='Код', required=True, max_length=3)
    name = serializers.CharField(label='Название', required=True, max_length=255)
    rate = serializers.DecimalField(max_digits=10, decimal_places=5)
