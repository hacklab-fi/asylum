# -*- coding: utf-8 -*-
import rest_framework_filters as filters
from rest_framework import serializers, viewsets

from .models import RecurringTransaction, Transaction, TransactionTag


class TransactionTagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TransactionTag


class TransactionTagFilter(filters.FilterSet):

    class Meta:
        model = TransactionTag
        fields = {
            'label': filters.ALL_LOOKUPS,
        }


class TransactionTagViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionTagSerializer
    queryset = TransactionTag.objects.all()
    filter_class = TransactionTagFilter


class TransactionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionFilter(filters.FilterSet):

    class Meta:
        model = Transaction
        fields = {
            'stamp': filters.ALL_LOOKUPS,
            'tag': filters.ALL_LOOKUPS,
            'reference': filters.ALL_LOOKUPS,
            'owner': filters.ALL_LOOKUPS,
            'amount': filters.ALL_LOOKUPS,
            'unique_id': filters.ALL_LOOKUPS,
        }


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filter_class = TransactionFilter


class RecurringTransactionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RecurringTransaction
        fields = '__all__'


class RecurringTransactionFilter(filters.FilterSet):

    class Meta:
        model = RecurringTransaction
        fields = {
            'start': filters.ALL_LOOKUPS,
            'end': filters.ALL_LOOKUPS,
            'label': filters.ALL_LOOKUPS,
            'rtype': filters.ALL_LOOKUPS,
            'tag': filters.ALL_LOOKUPS,
            'owner': filters.ALL_LOOKUPS,
            'amount': filters.ALL_LOOKUPS,
        }


class RecurringTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = RecurringTransactionSerializer
    queryset = RecurringTransaction.objects.all()
    filter_class = RecurringTransactionFilter
