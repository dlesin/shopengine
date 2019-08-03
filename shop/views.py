from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import *
from django.http import JsonResponse
from decimal import Decimal


def get_cart(request):
    if request.session.get('cart_id'):
        cart = Cart.objects.get(id=request.session.get('cart_id'))
        request.session['total'] = cart.items.count()
        return cart
    else:
        cart = Cart()
        cart.save()
        request.session['cart_id'] = cart.id
        cart = Cart.objects.get(id=request.session['cart_id'])
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
    return render(request, 'home.html', context=context)


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
    categories = Category.objects.all()
    products_of_category = Product.objects.filter(category=category)
    context = {
        'categories': categories,
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
    new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
    if new_item not in cart.items.all():
        cart.items.add(new_item)
        cart.save()
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
    for cart_item in cart.items.all():
        if cart_item.product == product:
            cart.items.remove(cart_item)
            cart.save()
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
    if cart.items.count() == 0:
        return redirect('base_view_url', permanent=True)
    items_in_cart = cart.items.all()
    items_in_order = '\n'.join([str(item_in_cart) for item_in_cart in items_in_cart])
    form = OrderForm(request.POST or None)
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
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
        request.session['order_id'] = new_order.id
        return redirect('thanks_view_url', permanent=True)


def thanks_view(request):
    order_id = request.session['order_id']
    context = {
        'id': order_id
    }
    return render(request, 'thanks.html', context)
