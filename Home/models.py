from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.db.models import Sum
from PIL import Image



# Create your models here.
CATEGORY_CHOICES = (
    ('T','Tshirt'),
    ('S','Shirt'),
    ('B','Suits & Blazzers'),
    ('K','Kurtas'),
    ('BJ','Jeans'),
    ('BT','Trousers'),
    ('BS','Shorts'),
    ('BC','Cargos'),
    ('BP','Track pants')
)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='b2.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img= Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Men(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    image = models.ImageField(upload_to="gallery", default='Gallery/T2.jpg')
    description = models.CharField(max_length=500)
    slug = models.SlugField(blank=True,null=True)
    sleeve = models.CharField(max_length=50,blank=True,default='')
    necktype = models.CharField(max_length=50,blank=True,default='')
    color = models.CharField(max_length=50,blank=True,default='')
    febric= models.CharField(max_length=50,blank=True,default='')
    size = models.CharField(max_length=50,blank=True,default='L')
    fit = models.CharField(max_length=50,blank=True,default='Regular')

    def __str__(self):
        return self.title

    def get_Search_url(self):
        return reverse("Home:ItemDetail", kwargs={
            'slug': self.slug
        })
       
    def get_Shirt_url(self):
        return reverse("Home:ShirtDetail", kwargs={
            'slug': self.slug
        })

    def get_tshirt_url(self):
        return reverse("Home:TshirtDetail", kwargs={
            'slug': self.slug
        })

    def get_Blazzer_url(self):
        return reverse("Home:BlazzerDetail", kwargs={
            'slug': self.slug
        })

    def get_Cargo_url(self):
        return reverse("Home:CargoDetail", kwargs={
            'slug': self.slug
        })

    def get_Jeans_url(self):
        return reverse("Home:JeansDetail", kwargs={
            'slug': self.slug
        })

    def get_Kurta_url(self):
        return reverse("Home:KurtaDetail", kwargs={
            'slug': self.slug
        })

    def get_Shorts_url(self):
        return reverse("Home:ShortsDetail", kwargs={
            'slug': self.slug
        })

    def get_Track_url(self):
        return reverse("Home:TrackDetail", kwargs={
            'slug': self.slug
        })

    def get_Trouser_url(self):
        return reverse("Home:TrouserDetail", kwargs={
            'slug': self.slug
        })
    
    def get_add_to_cart_url(self):
        return reverse("Home:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("Home:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def discount_code(self):
        code=100
        ans=code - int((self.discount_price*100)/(self.price))
        return ans


    


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Men,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_savings(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()
        
    def final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        else:
            return self.get_total_item_price()
 
class Wishlist(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product= models.ForeignKey(Men,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.title


class Order(models.Model):
    items = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    cashpayment = models.ForeignKey(
        'Cash', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon',on_delete=models.SET_NULL, blank=True, null=True)

                                                                                    
    def __str__(self):
        return self.user.username

    def order_total_without_code(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.final_price()
        return total

    def order_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    contact = models.IntegerField(max_length=10)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Cash(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount= models.FloatField()

    def __str__(self):
        return self.code



