from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework.pagination import LimitOffsetPagination

from . import services
from .serializers import CurrencySerializer


class CurrencyList(APIView):
    serializer_class = CurrencySerializer
    pagination_class = LimitOffsetPagination

    def get(self, request):
        currencies = services.get_all_currencies()
        page = self.paginator.paginate_queryset(currencies, self.request, view=self)
        serializer = self.serializer_class(page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            self._paginator = self.pagination_class()
        return self._paginator


class CurrencyDetail(APIView):
    serializer_class = CurrencySerializer

    def get(self, request, pk, format=None):
        currency = self._get_object(pk)
        serializer = self.serializer_class(currency, context={'request': request})
        return Response(serializer.data)

    def _get_object(self, pk):
        try:
            currency = services.get_currency_by_id(pk)
        except services.EntityDoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, currency)
        return currency
