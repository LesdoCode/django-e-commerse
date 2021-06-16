from django import forms
from django.forms import ModelForm
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from .models import Item, Category, EFTPayment


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
    ('COD', 'Cash on delivery'),
)


class AddressForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField()
    country = CountryField().formfield(widget=CountrySelectWidget(
        {
            "class":"custom-select d-block w-100"
        }
    ))
    zip_code = forms.CharField()
    save_info = forms.BooleanField(required=False)
    default = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

class ItemFilterForm(forms.Form):
    category_choices = list(Category.objects.all())
    category = forms.ChoiceField( choices=[category_choices], required=False )

class ProofOfPaymentForm(ModelForm):
    class Meta:
        model = EFTPayment
        fields = [  'bank_name',
                    'amount',
                    'proof_of_payment'
                ]