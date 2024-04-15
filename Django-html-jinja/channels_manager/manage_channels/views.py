from django.shortcuts import render
from .models import Transaction, PaidContent


# Create your views here.
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request,
                  'transaction_list.html',
                  {'transactions': transactions}
                  )


def index(request):
    return render(request, 'index.html', )


def content_list(request):
    content = PaidContent.objects.all()
    return render(request, 'content_list.html', {'content': content})


def content_detail(request, pk):
    content = PaidContent.objects.get(pk=pk)
    return render(request, 'content_detail.html', {'content': content})

