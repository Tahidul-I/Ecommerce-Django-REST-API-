from django import forms
from .models import OurBestDeals, ProductVariation,MeherunSignature,BannerProducts
from ..banner.models import CarouselBanner
class OurBestDealsForm(forms.ModelForm):
    class Meta:
        model = OurBestDeals
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['products'].queryset = ProductVariation.objects.filter(is_deal=True)


class MeherunSignatureForm(forms.ModelForm):
    class Meta:
        model = MeherunSignature
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['products'].queryset = ProductVariation.objects.filter(is_signature=True)


class BannerProductsForm(forms.ModelForm):
    class Meta:
        model = BannerProducts
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['products'].queryset = ProductVariation.objects.filter(is_banner_product=True)
        self.fields['banner_obj'].queryset = CarouselBanner.objects.filter(is_active=True)
