from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from Home.views import Shirtview,Cargoview,MyOrderView,AddCouponView,indexView,searchFormView,priceFormView,SearchDetailView,\
Trackview,Trouserview,Tshirtview,Jeansview,Shortsview,Kurtaview,PaymentView,codView,\
Blazzerview,BlazzerDetailView,ShirtDetailView,TshirtDetailView,WishlistView,move_to_wishlist,remove_from_wishlist,\
BlazzerDetailView,CargoDetailView,JeansDetailView,ShortsDetailView,OrderSummaryView,empty_cart,\
KurtaDetailView,TrackDetailView,TrouserDetailView,add_to_cart,remove_from_cart,remove_single_item_from_cart,CheckoutView,profile

app_name = 'Home'

urlpatterns=[
    path('',indexView.as_view(),name="index"),
    path('index',indexView.as_view(),name="index"),
    path('Tshirt',Tshirtview.as_view(),name="Tshirt"),
    path('Shirt',Shirtview.as_view(),name="Shirt"),
    path('Blazzer',Blazzerview.as_view(),name="Blazzer"),
    path('Cargo',Cargoview.as_view(),name="Cargo"),
    path('Jeans',Jeansview.as_view(),name="Jeans"),
    path('Kurta',Kurtaview.as_view(),name="Kurta"),
    path('Shorts',Shortsview.as_view(),name="Shorts"),
    path('Trouser',Trouserview.as_view(),name="Trouser"),
    path('Track',Trackview.as_view(),name="Track"),
    path('ShirtDetail/<slug>/', ShirtDetailView.as_view(), name='ShirtDetail'),
    path('TshirtDetail/<slug>/', TshirtDetailView.as_view(), name='TshirtDetail'),
    path('BlazzerDetail/<slug>/',BlazzerDetailView.as_view(), name='BlazzerDetail'),
    path('CargoDetail/<slug>/', CargoDetailView.as_view(), name='CargoDetail'),
    path('JeansDetail/<slug>/', JeansDetailView.as_view(), name='JeansDetail'),
    path('KurtaDetail/<slug>/', KurtaDetailView.as_view(), name='KurtaDetail'),
    path('ShortsDetail/<slug>/', ShortsDetailView.as_view(), name='ShortsDetail'),
    path('TrackDetail/<slug>/', TrackDetailView.as_view(), name='TrackDetail'),
    path('TrouserDetail/<slug>/', TrouserDetailView.as_view(), name='TrouserDetail'),
    path('ItemDetail/<slug>/', SearchDetailView.as_view(), name='ItemDetail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('AddCoupon/', AddCouponView.as_view(), name='AddCoupon'),    
    path('move-to-wishlist/<slug>/',move_to_wishlist,name='move-to-wishlist'),
    path('remove-from-wishlist/<slug>/',remove_from_wishlist,name="remove-from-wishlist"),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('OrderSummary', OrderSummaryView.as_view(), name='OrderSummary'),
    path('Checkout', CheckoutView.as_view(), name='Checkout'),
    path('Profile', profile, name='profile'),
    path('Search', searchFormView.as_view(), name='Search'),
    path('Price', priceFormView.as_view(), name='Price'),
    path('MyOrder', MyOrderView.as_view(), name='MyOrder'),
    path('empty_cart', empty_cart, name='empty_cart'),
    path('Payment/<payment_option>/', PaymentView.as_view(), name='Payment'),
    path('Cod', codView.as_view(), name='Cod'),
    path('Wishlist', WishlistView.as_view(), name='Wishlist'),








    
    
                            
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

