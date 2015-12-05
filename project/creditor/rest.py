from rest_framework import viewsets, serializers
from .models import TransactionTag, Transaction, RecurringTransaction

class TransactionTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TransactionTag

class TransactionTagViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionTagSerializer
    queryset = TransactionTag.objects.all()

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

class RecurringTransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecurringTransaction

class RecurringTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = RecurringTransactionSerializer
    queryset = RecurringTransaction.objects.all()
