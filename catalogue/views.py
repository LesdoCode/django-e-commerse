from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, Address
from django.contrib import messages
from django.utils import timezone
from .forms import AddressForm, ItemFilterForm, ProofOfPaymentForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse


class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    paginate_by = 8
    

class ProductDetail(DetailView):
    model = Item
    template_name = 'products.html'


class OrderSummary(LoginRequiredMixin ,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            total = order.get_grand_total()
            context = {
                'order': order,
                'grand_total': total
            }
            return render (self.request, 'order_summary.html', context)
        except:
            messages.success(self.request, "You don't have an active order.")
            return redirect('home')


class CheckOutView(View):

    def get (self, *args, **kwargs):
        form = AddressForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        try:
            address = Address.objects.get(user=self.request.user, default=True)
            context = {
                'form': form,
                'address': address,
                'order': order,
            }
        except:
            context = {
                'form': form,
                'order': order,
            }
            
        return render (self.request, 'checkout.html', context)
    
    def post(self, *args, **kwargs):
        form = AddressForm(self.request.POST)
        order = Order.objects.get(user=self.request.user, ordered=False)
        is_cash_transfer = False
        
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip_code = form.cleaned_data.get('zip_code')
            save_info = form.cleaned_data.get('save_info')
            default = form.cleaned_data.get('default')
            use_default = form.cleaned_data.get('use_default')
            payment_option = form.cleaned_data.get('payment_option')

            address = Address(
                user = self.request.user,
                street_address = street_address,
                apartment_address = apartment_address,
                country = country,
                zip_code = zip_code,
                default = default,
                use_default = use_default,
                payment_option = payment_option,
            )

            address.save()
            if save_info:
                address.default = True
                address.save()
                order.address = address
                order.save()

            if use_default:
                address = Address.objects.get(user=self.request.user, default=True)
                order.address = address
                order.save()          
       
        return redirect('proof_of_pay')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        #if order item exists, increase quantity else add it to the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f"{item.title}'s quantity updated.")
            
        else:
            order.items.add(order_item)
            order_item.save()
            messages.success(request, f"{item.title} has been added to your cart.")      
        
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False, ordered_date=ordered_date)
        order.items.add(order_item)
        order.save()
        messages.success(request, f"{item.title} has been added to your cart.")
    
    return redirect('order_summary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        #if order item exists, increase quantity else add it to the order
        if order.items.filter(item__slug=item.slug).exists():
            order.items.remove(order_item)
            order_item.quantity = 1
            order_item.save()
            messages.success(request, f"{item.title} has been removed to your cart.")
            return redirect('order_summary')
            
        else:
            messages.success(request, f"{item.title} was not in your cart.")
            return redirect('product', slug=slug)

    else:
        messages.success(request, "You dont have an active order")
        return redirect('product', slug=slug)


@login_required
def remove_single_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        #if order item exists, increase quantity else add it to the order
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.success(request, f"{item.title} quantity reduced.")
                return redirect('order_summary')
            else:
                order.items.remove(order_item)
                messages.success(request, f"{item.title} has been removed to your cart.")
                return redirect('order_summary')
            
        else:
            messages.success(request, f"{item.title} was not in your cart.")
            return redirect('product', slug=slug)

    else:
        messages.success(request, "You dont have an active order")
        return redirect('product', slug=slug)


@login_required
def delivery(request):
    orders = Order.objects.filter(ordered=False)
    context = {
        'orders': orders
    }
    
    return render(request, "delivery.html", context)


def item_search(request):
    if request.method == "POST":
        search = request.POST['search']
        items = Item.objects.filter(search_terms__contains=search)

        context = {
            'search': search,
            'items': items
        }
        if search == "":
            return redirect('home')
        else:
            return render(request, 'item_search.html', context)


def filter(request):
    form = ItemFilterForm()
    return render(request, 'home.html', {'form': form})

@login_required
def proof_of_pay(request):
    form = ProofOfPaymentForm()
    if request.method == 'POST':
        print(request.POST)
        return redirect('order_success')


    context = {'form': form }
    return render(request, 'proof_of_pay.html', context)


def order_success(request):
    return render(request, 'order_success.html')

