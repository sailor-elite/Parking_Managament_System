from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from parking.models import Parking
from transactions.forms import TransactionForm
from transactions.models import Transaction


def transactions_view(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions.html', {'transactions': transactions})


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('home')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'add_transaction.html', {'form': form})
