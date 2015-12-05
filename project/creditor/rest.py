from rest_framework import viewsets, serializers
from .models import TransactionTag, Transaction, RecurringTransaction

class TransactionTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TransactionTag

class TransactionTagViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionTagSerializer
    queryset = TransactionTag.objects.all()
    filter_fields = ('label',)

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filter_fields = ('stamp','tag','reference','owner','amount','unique_id')

class RecurringTransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecurringTransaction

class RecurringTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = RecurringTransactionSerializer
    queryset = RecurringTransaction.objects.all()
    filter_fields = ('start','end','label','rtype','tag','owner','amount')
