from django import forms
from .models import RatePool

# class RatePoolUpdateForm(forms.ModelForm):
#     class Meta:
#         model = RatePool
#         fields = ['code', 'name', 'quantity']  
#         labels = {
#             'code': _("Rate Offer Product Code"),
#             'name': _("Rate Offer Product Name"),
#             'quantity': _("Quantity"),  
#         }


class RatePoolForm(forms.ModelForm):
    class Meta:
        model = RatePool
        fields = ['code', 'name', 'quantity']


from .models import RateType

class RateTypeForm(forms.ModelForm):
    class Meta:
        model = RateType
        fields = ['rate_type']
