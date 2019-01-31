# -*- coding: utf-8 -*-
import rest_framework_filters as filters
from rest_framework import serializers, viewsets

from .models import AccessType, Grant, Token, TokenType


class TokenTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TokenType


class TokenTypeFilter(filters.FilterSet):

    class Meta:
        model = TokenType
        fields = {
            'label': filters.ALL_LOOKUPS,
        }


class TokenTypeViewSet(viewsets.ModelViewSet):
    serializer_class = TokenTypeSerializer
    queryset = TokenType.objects.all()
    filter_class = TokenTypeFilter


class TokenSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Token
        fields = '__all__'


class TokenFilter(filters.FilterSet):

    class Meta:
        model = Token
        fields = {
            'label': filters.ALL_LOOKUPS,
            'owner': filters.ALL_LOOKUPS,
            'ttype': filters.ALL_LOOKUPS,
            'value': filters.ALL_LOOKUPS,
            'revoked': filters.ALL_LOOKUPS,
        }


class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = TokenSerializer
    queryset = Token.objects.all()
    filter_class = TokenFilter


class AccessTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AccessType
        fields = '__all__'


class AccessTypeFilter(filters.FilterSet):

    class Meta:
        model = AccessType
        fields = {
            'label': filters.ALL_LOOKUPS,
            'bit': filters.ALL_LOOKUPS,
            'external_id': filters.ALL_LOOKUPS,
        }


class AccessTypeViewSet(viewsets.ModelViewSet):
    serializer_class = AccessTypeSerializer
    queryset = AccessType.objects.all()
    filter_class = AccessTypeFilter


class GrantSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Grant
        fields = '__all__'


class GrantFilter(filters.FilterSet):

    class Meta:
        model = Grant
        fields = {
            'owner': filters.ALL_LOOKUPS,
            'atype': filters.ALL_LOOKUPS,
        }


class GrantViewSet(viewsets.ModelViewSet):
    serializer_class = GrantSerializer
    queryset = Grant.objects.all()
    filter_class = GrantFilter
