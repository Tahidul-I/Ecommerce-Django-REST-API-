from django.contrib import admin
from .models import *
from .forms import OurBestDealsForm,MeherunSignatureForm,BannerProductsForm

class ProductVariationInline(admin.StackedInline):
    model = ProductVariation
    
class ProductImagesInline(admin.StackedInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariationInline, ProductImagesInline]


class OurBestDealsAdmin(admin.ModelAdmin):
    form = OurBestDealsForm
    list_display = ('title',)
    search_fields = ('title',)

class MeherunSignatureadmin(admin.ModelAdmin):
    form = MeherunSignatureForm
    list_display = ('title',)
    search_fields = ('title',)

class BannerProductsadmin(admin.ModelAdmin):
    form = BannerProductsForm
    list_display = ('title',)
    search_fields = ('title',)


admin.site.register(Product,ProductAdmin)
admin.site.register(ProductVariation)
admin.site.register(ProductImages)
admin.site.register(OurBestDeals,OurBestDealsAdmin)
admin.site.register(MeherunSignature,MeherunSignatureadmin)
admin.site.register(BannerProducts,BannerProductsadmin)
admin.site.register(FrequentlyBroughtTogether)
admin.site.register(RecommendedProduct)
