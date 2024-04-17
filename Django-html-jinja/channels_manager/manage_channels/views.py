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


def content_detail(request, url):
    content_x = PaidContent.objects.get(url=url)
    return render(request, 'content_detail.html', {'content_x': content_x})
