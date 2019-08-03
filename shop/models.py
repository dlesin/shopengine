# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import reverse
from transliterate import translit


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={'category_slug': self.slug})


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(str(instance.name), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class Brand(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


# Переопределение objects.all()
# class ProductManager(models.Manager):
# 	def all(self, *args, **kwargs):
# 		return super(ProductManager, self).get_queryset().filter(available=True)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, db_index=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)
    
    #    objects = ProductManager()  Переопределение objects.all()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('product_detail_url', kwargs={'product_slug': self.slug})


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.qty} - {self.product.title}"


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Корзина  №{self.id}"
    
    def add_to_card(self, product_slug):
        cart = self
        product = Product.objects.get(slug__iexact=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()
    
    def remove_from_card(self, product_slug):
        cart = self
        product = Product.objects.get(slug__iexact=product_slug)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()


ORDER_STATUS_CHOICES = (
    ('Обработка', 'Обработка'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен'),
)

BUYING_TYPE = (
    ('self', 'Самовывоз'),
    ('delivery', 'Доставка'),
)


class Order(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ForeignKey(Cart, on_delete=models.CASCADE)
    items_in_order = models.TextField()
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    status = models.CharField(max_length=60, choices=ORDER_STATUS_CHOICES, default='Обработка')
    buying_type = models.CharField(max_length=40, choices=BUYING_TYPE, default='Самовывоз')
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Заказ №{0}".format(str(self.id))
