from django.shortcuts import render

from parking.models import Parking
from transactions.models import Transaction


# Create your views here.

def transactions_view(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions.html', {'transactions': transactions})
