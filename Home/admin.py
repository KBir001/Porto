from django.contrib import admin
from .models import Men,Cart,Order,BillingAddress,Payment,Wishlist,Coupon,Profile
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'ordered'
    ]
class MenAdmin(admin.ModelAdmin):
    list_display=[
        'title',
        'slug'
    ]
admin.site.register(Men,MenAdmin)
admin.site.register(Cart)
admin.site.register(Order,OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Wishlist)
admin.site.register(Coupon)
admin.site.register(Profile)