from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import *
from django.http import JsonResponse
from decimal import Decimal


def get_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
        return cart
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
        return cart

def base_view(request):
    cart = get_cart(request)
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    context = {
        'categories': categories,
        'products': products,
        'cart': cart,
    }
    return render(request, 'base.html', context=context)


def product_view(request, product_slug):
    cart = get_cart(request)
    product = Product.objects.get(slug__iexact=product_slug)
    context = {
        'product': product,
        'cart': cart,
    }
    return render(request, 'product.html', context=context)


def category_view(request, category_slug):
    category = Category.objects.get(slug__iexact=category_slug)
    products_of_category = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products_of_category': products_of_category
    }
    return render(request, 'category.html', context=context)


def cart_view(request):
    cart = get_cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'cart.html', context=context)


def add_to_cart_view(request):
    cart = get_cart(request)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug__iexact=product_slug)
    cart.add_to_card(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def remove_from_cart_view(request):
    cart = get_cart(request)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug__iexact=product_slug)
    cart.remove_from_card(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def change_item_qty(request):
    cart = get_cart(request)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart_item = CartItem.objects.get(id=int(item_id))
    cart_item.qty = int(qty)
    cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
    cart_item.save()
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({
        'cart_total': cart.items.count(),
        'item_total': cart_item.item_total,
        'cart_total_price': cart.cart_total
    })


def checkout_view(request):
    cart = get_cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'checkout.html', context=context)


def order_create_view(request):
    cart = get_cart(request)
    form = OrderForm(request.POST or None)
    context = {
        'form': form,
        'cart': cart
    }
    return render(request, 'order.html', context=context)


def make_order_view(request):
    cart = get_cart(request)
    items_in_cart = cart.items.all()
    items_in_order = '\n'.join([str(item_in_cart) for item_in_cart in items_in_cart])
    form = OrderForm(request.POST or None)
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        print (buying_type)
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        new_order = Order()
        new_order.items = cart
        new_order.items_in_order = items_in_order
        new_order.first_name = first_name
        new_order.last_name = last_name
        new_order.phone = phone
        new_order.buying_type = buying_type
        new_order.address = address
        new_order.comments = comments
        new_order.total = cart.cart_total
        new_order.save()
        del request.session['cart_id']
        del request.session['total']
        return redirect('thanks_view_url', permanent=True)


def thanks_view(request):
    return render(request, 'thanks.html')
