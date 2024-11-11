from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['vehicle', 'user', 'transactionTimestamp', 'parking', 'zone']
