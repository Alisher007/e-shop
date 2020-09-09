from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from orders.models import Order
from decouple import config

import stripe

stripe.api_key = config('STRIPE_KEY')

# Create your views here.

def index(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    amount = "{:.2f}".format(order.get_total_cost())
    return render(request, 'payment/payment.html', {"order": amount, "name": order.first_name})

def charge(request):

    if request.method == 'POST':
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)

        customer = stripe.Customer.create(
            email = order.email,
            name = order.first_name,
            source=request.POST['stripeToken']
            )

        charge = stripe.Charge.create(
            customer=customer,
            amount= int(order.get_total_cost() * 100),
            currency='usd',
            description="Donation"
            )

    return redirect(reverse('payment:success'))

def successMsg(request):
    return render(request, 'payment/success.html')
