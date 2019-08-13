from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from shop.forms import OrderForm
from shop.models import *
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
        cart = Cart.objects.get(id=request.session.get('cart_id'))
        return cart


class HomeView(ListView):
    model = Product
    queryset = Product.objects.filter(available=True)
    template_name = 'home.html'
    context_object_name = 'products_list'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        context['cart'] = get_cart(self.request)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        cart = get_cart(self.request)
        product = Product.objects.get(slug__iexact=self.kwargs.get('slug'))
        context['product_in_cart'] = cart.items.filter(product=product).exists()
        context['cart'] = cart
        return context


class CategoryDetailView(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'


    def get_context_data(self, **kwargs):        
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        category = Category.objects.get(slug__iexact=self.kwargs.get('slug'))
        context['products_of_category'] = Product.objects.filter(category=category)
        context['cart'] = get_cart(self.request)
        return context


class CartView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'cart': get_cart(self.request)
        }
        return render(request, 'cart.html', context)


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        cart = get_cart(self.request)
        product_slug = request.GET.get('product_slug')
        print(product_slug)
        product = Product.objects.get(slug__iexact=product_slug)
        print(product)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        print(new_item, _)
        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()
        return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


# def add_to_cart_view(request):
#     cart = get_cart(request)
#     product_slug = request.GET.get('product_slug')
#     product = Product.objects.get(slug__iexact=product_slug)
#     new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
#     if new_item not in cart.items.all():
#         cart.items.add(new_item)
#         cart.save()
#     new_cart_total = 0.00
#     for item in cart.items.all():
#         new_cart_total += float(item.item_total)
#     cart.cart_total = new_cart_total
#     cart.save()
#     return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


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


class OrderView(View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(self.request.POST or None)
        context = {
            'form': form,
            'cart': get_cart(self.request)
        }
        return render(request, 'order.html', context=context)

    def post(self, request, *args, **kwargs):
        cart = get_cart(self.request)
        if cart.items.count() == 0:
            return redirect('base_view_url', permanent=True)
        items_in_order = '\n'.join([str(item_in_cart) for item_in_cart in cart.items.all()])
        form = OrderForm(self.request.POST or None)
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


class ThanksView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'id': self.request.session['order_id']
        }
        return render(request, 'thanks.html', context)









# def checkout_view(request):
#     cart = get_cart(request)
#     context = {
#         'cart': cart
#     }
#     return render(request, 'checkout.html', context=context)