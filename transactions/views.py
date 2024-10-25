from django.shortcuts import render

from transactions.models import Transaction


# Create your views here.

def transactions_view(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions.html', {'transactions': transactions})
