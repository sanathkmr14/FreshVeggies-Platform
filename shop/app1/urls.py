from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm


urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('product_detail/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),

    path('buy/', views.buy_now, name='buy-now'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('create-paypal-payment/', views.create_paypal_payment, name='create_paypal_payment'),
    path('capture-paypal-payment/', views.capture_paypal_payment, name='capture_paypal_payment'),
    path('place-order-cod/', views.place_order_cod, name='place_order_cod'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm),name='login' ),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout' ),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('add-address/', views.AddAddressView.as_view(), name='add-address'),
    path('updateAddress/<int:pk>', views.UpdateAddressView.as_view(), name='updateAddress'),
    path('deleteAddress/<int:pk>', views.delete_address, name='deleteAddress'),
    #path('changepassword/', views.change_password, name='changepassword'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('orders/', views.orders, name='orders'),
    path('contact', views.contact, name='contact'),
    path('search/', views.search, name='search')

    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)