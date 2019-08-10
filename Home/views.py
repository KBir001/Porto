from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import ListView,DeleteView,View,DetailView,TemplateView,FormView
from .models import Men,Cart,Order,BillingAddress,Payment,Wishlist,Coupon,Cash
from .form import CheckoutForm,CouponForm,SearchForm,PriceForm,UserUpdateForm,ProfileUpdateForm
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q


import random
import string
import stripe
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc" 
    
# Create your views here.
class indexView(TemplateView):
    template_name = "Men/index.html"
    def get(self,request, *args,**kwargs):
        try:
            search_form = SearchForm(self.request.GET or None)
            price_form = PriceForm(self.request.GET or None)
            item=Men.objects.all()
            context={
                'object':item,
                'search_form':search_form,
                'price_form':price_form
            }
            return self.render_to_response(context)
        except ObjectDoesNotExist:
            messages.info(self.request,"no data found")

class searchFormView(FormView): 
    
    form_class=SearchForm
    template_name = "Men/Search.html"
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        try:
            if form.is_valid():
                search=form.cleaned_data.get('data')
                search_form = SearchForm(self.request.GET or None)
                price_form = PriceForm(self.request.GET or None)
                if search=='shirt':
                    con=Men.objects.filter(category='S')
                    context={
                        'object':con,
                        'search_form':search_form,
                        'price_form':price_form                   
                    }
                elif search=='blazzer':
                    con=Men.objects.filter(category='B')
                    context={
                        'object':con,
                        'search_form':search_form,
                        'price_form':price_form                   
                    }
                else:
                    con=Men.objects.filter(title__icontains=search)
                    context={
                        'object':con,
                        'search_form':search_form,
                        'price_form':price_form                   
                    }
                return render(self.request,"Men/Search.html",context)
            else:
                return render(self.request, 'Men/index.html', 
                          {'search_form': search_form})

        except ObjectDoesNotExist:
            messages.info(self.request,"No match found")

class priceFormView(FormView): 
    
    form_class=PriceForm
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        search_form = SearchForm(self.request.GET or None)
        price_form = PriceForm(self.request.GET or None)
        try:
            if form.is_valid():
                small=form.cleaned_data.get('min_price')
                big=form.cleaned_data.get('max_price')
                con=Men.objects.filter(Q(discount_price__lte=big) & Q(discount_price__gte=small)) 
                context={
                    'object':con,
                    'search_form':search_form,
                    'price_form':price_form                   
                }
                return render(self.request,"Men/index.html",context)

        except ObjectDoesNotExist:
            messages.info(self.request,"No match found")

class Tshirtview(ListView):
    model=Men
    context_object_name = 'tshirt'
    paginate_by = 6
    template_name = "Men/Tshirt.html"

    def get_queryset(self):
        return Men.objects.filter(category='T')

    def get_context_data(self,**kwargs):
        context = super(Tshirtview,self).get_context_data(**kwargs)
        context['price_form']=PriceForm(self.request.GET or None)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

    def post(self,request,*args,**kwargs):
        search_form = SearchForm(self.request.GET or None)
        price_form = PriceForm(self.request.GET or None)
        try:
            form = PriceForm(self.request.POST or None)
            if form.is_valid():
                small=form.cleaned_data.get('min_price')
                big=form.cleaned_data.get('max_price')
                con=Men.objects.filter(Q(category='T') &Q(discount_price__lte=big) & Q(discount_price__gte=small)) 
                context={
                    'tshirt':con,
                    'search_form':search_form,
                    'price_form':price_form                   
                }
                return render(self.request,"Men/Tshirt.html",context)

        except ObjectDoesNotExist:
            messages.info(self.request,"No match found")

    


class Shirtview(ListView):
    model = Men
    context_object_name = 'shirt'
    paginate_by = 6
    template_name = "Men/Shirt.html"
    def get_queryset(self):
        return Men.objects.filter(category='S')

    def get_context_data(self,**kwargs):
        context = super(Shirtview,self).get_context_data(**kwargs)
        context['price_form']=PriceForm(self.request.GET or None)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

    def post(self,request,*args,**kwargs):
        search_form = SearchForm(self.request.GET or None)
        price_form = PriceForm(self.request.GET or None)
        try:
            form = PriceForm(self.request.POST or None)
            if form.is_valid():
                small=form.cleaned_data.get('min_price')
                big=form.cleaned_data.get('max_price')
                con=Men.objects.filter(Q(category='S') & Q(discount_price__lte=big) & Q(discount_price__gte=small)) 
                context={
                    'shirt':con,
                    'search_form':search_form,
                    'price_form':price_form                   
                }
                return render(self.request,"Men/Shirt.html",context)

        except ObjectDoesNotExist:
            messages.info(self.request,"No match found")


class Shortsview(ListView):
    model = Men
    context_object_name = 'shorts'
    paginate_by = 6
    template_name = "Men/Shorts.html"
    def get_queryset(self):
        return Men.objects.filter(category='BS')

    def get_context_data(self,**kwargs):
        context = super(Shortsview,self).get_context_data(**kwargs)
        context['price_form']=PriceForm(self.request.GET or None)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

    def post(self,request,*args,**kwargs):
        search_form = SearchForm(self.request.GET or None)
        price_form = PriceForm(self.request.GET or None)
        try:
            form = PriceForm(self.request.POST or None)
            if form.is_valid():
                small=form.cleaned_data.get('min_price')
                big=form.cleaned_data.get('max_price')
                con=Men.objects.filter(Q(category='BS') &Q(discount_price__lte=big) & Q(discount_price__gte=small)) 
                context={
                    'shorts':con,
                    'search_form':search_form,
                    'price_form':price_form                   
                }
                return render(self.request,"Men/Shorts.html",context)

        except ObjectDoesNotExist:
            messages.info(self.request,"No match found")

class Blazzerview(ListView):
    model = Men
    context_object_name = 'blazzer'
    paginate_by = 6
    template_name = "Men/Blazzer.html"

    def get_queryset(self):
        return Men.objects.filter(category='B')

    def get_context_data(self,**kwargs):
        context = super(Blazzerview,self).get_context_data(**kwargs)
        context['price_form']=PriceForm(self.request.GET or None)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

    def post(self,request,*args,**kwargs):
        search_form = SearchForm(self.request.GET or None)
        price_form = PriceForm(self.request.GET or None)
        try:
            form = PriceForm(self.request.POST or None)
            if form.is_valid():
                small=form.cleaned_data.get('min_price')
                big=form.cleaned_data.get('max_price')
                con=Men.objects.filter(Q(category='B') &Q(discount_price__lte=big) & Q(discount_price__gte=small)) 
                context={
                    'blazzer':con,
                    'search_form':search_form,
                    'price_form':price_form                   
                }
                return render(self.request,"Men/Blazzer.html",context)

        except ObjectDoesNotExist:
            messages.info(self.request,"No match found")

class Cargoview(ListView):
    model = Men
    context_object_name = 'cargo'
    paginate_by = 6
    template_name = "Men/Cargo.html"

    def get_queryset(self):
        return Men.objects.filter(category='BC')

    def get_context_data(self,**kwargs):
        context = super(Cargoview,self).get_context_data(**kwargs)
        context['price_form']=PriceForm(self.request.GET or None)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

    def post(self,request,*args,**kwargs):
        search_form = SearchForm(self.request.GET or None)
        price_form = PriceForm(self.request.GET or None)
        try:
            form = PriceForm(self.request.POST or None)
            if form.is_valid():
                small=form.cleaned_data.get('min_price')
                big=form.cleaned_data.get('max_price')
                con=Men.objects.filter(Q(category='BC') &Q(discount_price__lte=big) & Q(discount_price__gte=small)) 
                context={
                    'cargo':con,
                    'search_form':search_form,
                    'price_form':price_form                   
                }
                return render(self.request,"Men/Cargo.html",context)

        except ObjectDoesNotExist:
            messages.info(self.request,"No match found")

class Jeansview(ListView):
    model = Men
    context_object_name = 'jeans'
    paginate_by = 6
    template_name = "Men/Jeans.html"

    def get_queryset(self):
        return Men.objects.filter(category='BJ')

    def get_context_data(self,**kwargs):
        context = super(Jeansview,self).get_context_data(**kwargs)
        context['price_form']=PriceForm(self.request.GET or None)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

    def post(self,request,*args,**kwargs):
        search_form = SearchForm(self.request.GET or None)
        price_form = PriceForm(self.request.GET or None)
        try:
            form = PriceForm(self.request.POST or None)
            if form.is_valid():
                small=form.cleaned_data.get('min_price')
                big=form.cleaned_data.get('max_price')
                con=Men.objects.filter(Q(category='BJ') & Q(discount_price__lte=big) & Q(discount_price__gte=small)) 
                context={
                    'jeans':con,
                    'search_form':search_form,
                    'price_form':price_form                   
                }
                return render(self.request,"Men/Jeans.html",context)

        except ObjectDoesNotExist:
            messages.info(self.request,"No match found")

class Kurtaview(ListView):
    model = Men
    context_object_name = 'kurta'
    paginate_by = 6
    template_name = "Men/Kurta.html"

    def get_queryset(self):
        return Men.objects.filter(category='K')

    def get_context_data(self,**kwargs):
        context = super(Kurtaview,self).get_context_data(**kwargs)
        context['price_form']=PriceForm(self.request.GET or None)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

    def post(self,request,*args,**kwargs):
        search_form = SearchForm(self.request.GET or None)
        price_form = PriceForm(self.request.GET or None)
        try:
            form = PriceForm(self.request.POST or None)
            if form.is_valid():
                small=form.cleaned_data.get('min_price')
                big=form.cleaned_data.get('max_price')
                con=Men.objects.filter(Q(category='K') & Q(discount_price__lte=big) & Q(discount_price__gte=small)) 
                context={
                    'kurta':con,
                    'search_form':search_form,
                    'price_form':price_form                   
                }
                return render(self.request,"Men/Kurta.html",context)

        except ObjectDoesNotExist:
            messages.info(self.request,"No match found")

class Trackview(ListView):
    model = Men
    context_object_name = 'track'
    paginate_by = 6
    template_name = "Men/Track.html"

    def get_queryset(self):
        return Men.objects.filter(category='BP')

    def get_context_data(self,**kwargs):
        context = super(Trackview,self).get_context_data(**kwargs)
        context['price_form']=PriceForm(self.request.GET or None)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

    def post(self,request,*args,**kwargs):
        search_form = SearchForm(self.request.GET or None)
        price_form = PriceForm(self.request.GET or None)
        try:
            form = PriceForm(self.request.POST or None)
            if form.is_valid():
                small=form.cleaned_data.get('min_price')
                big=form.cleaned_data.get('max_price')
                con=Men.objects.filter(Q(category='BP') & Q(discount_price__lte=big) & Q(discount_price__gte=small)) 
                context={
                    'track':con,
                    'search_form':search_form,
                    'price_form':price_form                   
                }
                return render(self.request,"Men/Track.html",context)

        except ObjectDoesNotExist:
            messages.info(self.request,"No match found")

class Trouserview(ListView):
    model = Men
    context_object_name = 'trouser'
    paginate_by = 6
    template_name = "Men/Trouser.html"
    
    def get_queryset(self):
        return Men.objects.filter(category='BT')

    def get_context_data(self,**kwargs):
        context = super(Trouserview,self).get_context_data(**kwargs)
        context['price_form']=PriceForm(self.request.GET or None)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

    def post(self,request,*args,**kwargs):
        search_form = SearchForm(self.request.GET or None)
        price_form = PriceForm(self.request.GET or None)
        try:
            form = PriceForm(self.request.POST or None)
            if form.is_valid():
                small=form.cleaned_data.get('min_price')
                big=form.cleaned_data.get('max_price')
                con=Men.objects.filter(Q(category='BT') & Q(discount_price__lte=big) & Q(discount_price__gte=small)) 
                context={
                    'trouser':con,
                    'search_form':search_form,
                    'price_form':price_form                   
                }
                return render(self.request,"Men/Trouser.html",context)

        except ObjectDoesNotExist:
            messages.info(self.request,"No match found")


class ShirtDetailView(DetailView):
    model = Men
    template_name = "Men/ShirtDetail.html"
    def get_queryset(self):
        return Men.objects.filter(category='S')

    def get_context_data(self,**kwargs):
        context = super(ShirtDetailView,self).get_context_data(**kwargs)
        context['search_form']=SearchForm(self.request.GET or None)
        return context


class TshirtDetailView(DetailView):
    model = Men
    template_name = "Men/TshirtDetail.html"
    def get_queryset(self):
        return Men.objects.filter(category='T')

    def get_context_data(self,**kwargs):
        context = super(TshirtDetailView,self).get_context_data(**kwargs)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

class BlazzerDetailView(DetailView):
    model = Men
    template_name = "Men/BlazzerDetail.html"
    def get_queryset(self):
        return Men.objects.filter(category='B')

    def get_context_data(self,**kwargs):
        context = super(BlazzerDetailView,self).get_context_data(**kwargs)
        context['search_form']=SearchForm(self.request.GET or None)
        return context


class CargoDetailView(DetailView):
    model = Men
    template_name = "Men/CargoDetail.html"
    def get_queryset(self):
        return Men.objects.filter(category='BC')

    def get_context_data(self,**kwargs):
        context = super(CargoDetailView,self).get_context_data(**kwargs)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

class JeansDetailView(DetailView):
    model = Men
    template_name = "Men/JeansDetail.html"
    def get_queryset(self):
        return Men.objects.filter(category='BJ')

    def get_context_data(self,**kwargs):
        context = super(JeansDetailView,self).get_context_data(**kwargs)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

class KurtaDetailView(DetailView):
    model = Men
    template_name = "Men/KurtaDetail.html"
    def get_queryset(self):
        return Men.objects.filter(category='K')

    def get_context_data(self,**kwargs):
        context = super(KurtaDetailView,self).get_context_data(**kwargs)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

class ShortsDetailView(DetailView):
    model = Men
    template_name = "Men/ShortsDetail.html"
    def get_queryset(self):
        return Men.objects.filter(category='BS')

    def get_context_data(self,**kwargs):
        context = super(ShortsDetailView,self).get_context_data(**kwargs)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

class TrackDetailView(DetailView):
    model = Men
    template_name = "Men/TrackDetail.html"
    def get_queryset(self):
        return Men.objects.filter(category='BP')

    def get_context_data(self,**kwargs):
        context = super(TrackDetailView,self).get_context_data(**kwargs)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

class TrouserDetailView(DetailView):
    model = Men
    template_name = "Men/TrouserDetail.html"
    def get_queryset(self):
        return Men.objects.filter(category='BT')

    def get_context_data(self,**kwargs):
        context = super(TrouserDetailView,self).get_context_data(**kwargs)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

class SearchDetailView(DetailView):
    model = Men
    template_name="Men/ItemDetail.html"
    def get_queryset(self):
        return Men.objects.all

    def get_context_data(self,**kwargs):
        context = super(SearchDetailView,self).get_context_data(**kwargs)
        context['search_form']=SearchForm(self.request.GET or None)
        return context

class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwarg):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            form = CouponForm()
            context = {
                'object': order,
                'form':form
            }
            return render(self.request,"Men/OrderSummary.html",context)
        except ObjectDoesNotExist:
            messages.error(self.request,"No items in your cart")
            return redirect("/")

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your Account has been Updated!')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
         'u_form':u_form,
         'p_form':p_form
    }

    return render(request,"Men/Profile.html",context)

class WishlistView(LoginRequiredMixin,View):
    def get(self,*args,**kwarg):
        try:
            wish = Wishlist.objects.filter(user = self.request.user)
            search_form = SearchForm(self.request.GET or None)
            context ={
                'object':   wish,
                'search_form':search_form
            }
            return render(self.request,"Men/Wishlist.html",context)
        except ObjectDoesNotExist:
            messages.error(self.request,"No products in your Wishlist")
            return redirect("/")

class MyOrderView(LoginRequiredMixin,View):
    def get(self,*args,**kwarg):
        try:
            order = Cart.objects.filter(user=self.request.user,ordered=True)
            context ={
                'object':order
            }
            return render(self.request,"Men/Myorder.html",context)
        except ObjectDoesNotExist:
            messages.error(self.request,"No active order found")
            return redirect("/")


@login_required
def move_to_wishlist(request, slug):
        item = get_object_or_404(Men,slug=slug)
        wished,created = Wishlist.objects.get_or_create(
            product=item,
            user=request.user
        )
        order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = Cart.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                order.items.remove(order_item)
        wish_qs = Wishlist.objects.filter(user = request.user,product__slug = item.slug)
        if wish_qs.exists():
                messages.info(request,"Product already exist in wishlist")
                return redirect("Home:Wishlist")
        else:
            witem = Wishlist.objects.create(user=request.user)
            witem.products.add(wished)
            messages.info(request, "Product was added to your wishlist.")
            return redirect("Home:Wishlist")

@login_required
def remove_from_wishlist(request, slug):
        item = get_object_or_404(Men,slug=slug)
        rem_qs= Wishlist.objects.filter(
            user=request.user,
        )
        if rem_qs.exists():
            Wishlist.objects.filter(product__slug=item.slug).delete()
            messages.info(request,"Item removed from wishlist")
            return redirect("Home:Wishlist")
        else:
            messages.info(request,"No products in Wishlist")
            return redirect("Home:Wishlist")
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Men,slug=slug)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("Home:OrderSummary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("Home:OrderSummary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("Home:OrderSummary")


@login_required
def empty_cart(request):
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        Order.objects.all().delete()
        messages.info(request,"All the item have been removed")
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.info(request,"No items found in cart")
        return redirect(request.META['HTTP_REFERER'])

        

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Men, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            if order.coupon:
                order.coupon = None
                order.save()
            messages.info(request, "This item was removed from your cart.")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.info(request, "This item was not in your cart")
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.info(request, "You do not have an active order")
        return redirect(request.META['HTTP_REFERER'])

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Men, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item) 
                if order.coupon:
                    order.coupon = None
                    order.save()
                messages.info(request, "This item quantity was updated.")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.info(request, "This item was not in your cart")
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.info(request, "You do not have an active order")
        return redirect(request.META['HTTP_REFERER'])

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order':order
                }
            return render(self.request, "Men/Checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("Home:index")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                contact = form.cleaned_data.get('contact')
                # TODO: add functionality for these fields
                # same_shipping_address = form.cleaned_data.get(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                    contact=contact
                )
                billing_address.save()
                order.billing_address = billing_address
                
                order.save()
                if payment_option == 'S':
                    return redirect('Home:Payment', payment_option='stripe')
                elif payment_option == 'C':
                    return redirect('Home:Cod')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('Home:Checkout')
                
                
            
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("Home:OrderSummary")



class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('coupon')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                coupon = Coupon.objects.get(code=code)
                check = Order.objects.filter(
                    user=self.request.user, ordered=True)
                if check.exists():
                    c1 = check[0]
                    if c1.coupon==coupon:
                        messages.info(self.request,"Coupon is already used")
                        return redirect("Home:OrderSummary")
                    else:
                        order.coupon = coupon
                        order.save()
                        messages.success(self.request,"Coupon applied successfully ")
                        return redirect("Home:OrderSummary")
                else:
                    order.coupon = coupon
                    order.save()
                    messages.success(self.request,"Coupon applied successfully ")
                    return redirect("Home:OrderSummary")
            except ObjectDoesNotExist:
                messages.info(self.request, "Invalid coupon code")
                return redirect("Home:OrderSummary")     

class codView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
            }
            return render(self.request, "Men/Cod.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("Home:Checkout")
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        try:
            # create the cash payment
            cash = Cash()
            cash.user = self.request.user
            cash.amount = order.order_total()
            cash.save()

            # assign the payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.cashpayment = cash
            order.save()
            messages.success(self.request, "Your order was successful!")
            send_mail(
                        'Order Placed',
                        'We have successfully received your order of . It will be deleivered soon.thank you for shopping with us.',
                        settings.EMAIL_HOST_USER,
                        [self.request.user.email],
                        fail_silently=False,
                    )
            
            return redirect("/")
        except ObjectDoesNotExist:
            messages.info(self.request,"something went wrong")
            return redirect("Home:OrderSummary")

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
            }
            return render(self.request, "Men/Payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("Home:Checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.order_total()* 100)

        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.order_total()
            payment.save()

            # assign the payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            #order.ref_code = create_ref_code()
            order.save()
            messages.success(self.request, "Your order was successful!")
            send_mail(
                        'Order Placed',
                        'We have successfully received your order of . It will be deleivered soon.thank you for shopping with us.',
                        settings.EMAIL_HOST_USER,
                        [self.request.user.email],
                        fail_silently=False,
                    )
            
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.warning(
                self.request, "A serious error occurred. We have been notifed.")
            return redirect("/")








    