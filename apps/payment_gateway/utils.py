from sslcommerz_lib import SSLCOMMERZ 
from ..order.models import ShippingDetails
from django.urls import reverse
def payment_gateway(order,indicator):
    shipping = ShippingDetails.objects.get(order = order)
    settings = { 'store_id': 'kuber65d9c2a23469f', 'store_pass': 'kuber65d9c2a23469f@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    payment_data = {}
    payment_data['total_amount'] = order.total_amount
    payment_data['currency'] = "BDT"
    if indicator == 'checkout':
        payment_data['tran_id'] ={order.tracking_no}
    else:
        payment_data['tran_id'] = f'#{order.tracking_no}'
    payment_data['order_id'] = order.id
    payment_data['success_url'] = f'https://meherun.abroadportals.com' + f"{reverse('payment_success')}"
    payment_data['fail_url'] = 'https://www.walmart.com/'
    payment_data['cancel_url'] = 'https://www.walmart.com/'
    payment_data['emi_option'] = 0
    payment_data['cus_name'] = order.name
    payment_data['cus_email'] = order.email
    payment_data['cus_phone'] = order.phone
    payment_data['ship_name' ] = order.name
    payment_data['ship_add1' ] = shipping.address
    payment_data['ship_city' ] = shipping.city
    payment_data['ship_country' ] = shipping.country
    payment_data['ship_postcode' ] = f"None"
    payment_data['cus_add1'] = order.address
    payment_data['cus_city'] = order.city
    payment_data['cus_country'] = order.country
    payment_data['shipping_method'] = "YES"
    payment_data['multi_card_name'] = ""
    payment_data['num_of_item'] = order.order_item.count()
    payment_data['product_name'] = "Test"
    payment_data['product_category'] = "Mixed"
    payment_data['product_profile'] = "general"
    print(payment_data)
    response = sslcz.createSession(payment_data)
    print(response)
    return response['GatewayPageURL']
