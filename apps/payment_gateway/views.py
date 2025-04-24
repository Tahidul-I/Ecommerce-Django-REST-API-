from django.shortcuts import redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
# Create your views here.
@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('tran_id')
        if transaction_id[0] == '#':
            transaction_id = int(transaction_id[1:])
            return redirect(f'https://meherunbeauty.abroadportals.com/checkout/subscription_complete?transaction_id={transaction_id}')
        else:
            return redirect(f'https://meherunbeauty.abroadportals.com/checkout/order_complete?transaction_id={int(transaction_id)}')

    # Handle invalid requests
    return HttpResponse("Invalid request", status=400)
