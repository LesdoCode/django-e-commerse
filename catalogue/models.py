from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django_countries.fields import CountryField
from .scripts.order_processor import generate_order_id


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sportwear'),
    ('OW', 'Outwear'),
)

LABEL_CHOICES = (
    ('S', 'secondary'),
    ('P', 'primary'),
    ('D', 'danger'),
)

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
    ('COD', 'Cash on delivery'),
)


class Category(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=200)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2, default='S')
    description = models.TextField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='static/images')
    search_terms = models.TextField(null=True, blank=True)
    stock_items = models.IntegerField(default=0)
    on_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug':self.slug} )

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'slug':self.slug} )

    def get_remove_single_from_cart_url(self):
        return reverse('remove_single_from_cart', kwargs={'slug':self.slug} )
    

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price() 


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True)
    address = models.ForeignKey("Address", on_delete=models.SET_NULL, blank=True, null=True)
    #order_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return generate_order_id(self)

    def get_grand_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_final_price()
        
        return total


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    apartment_address = models.CharField(max_length=200)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=200)
    save_info = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    use_default = models.BooleanField(default=False)
    payment_option = models.CharField(choices=PAYMENT_CHOICES, max_length=3)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.user.username

class EFTPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    proof_of_payment = models.ImageField(upload_to='static/images')
    
