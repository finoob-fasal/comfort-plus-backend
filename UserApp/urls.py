from django.urls import path
from UserApp import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    
    path("signup/", views.user_signup, name="user_signup"),
    path("login/", views.user_login, name="user_login"),

    #*********************PROFILE***********************

    path("view_profile/", views.view_profile, name="view_profile"),
    path("update_profile/", views.update_profile, name="update_profile"),
     path("api/token/refresh/",TokenRefreshView.as_view(), name="token_refresh"),

    #*********************SERVICES***********************

    path("view_services",views.view_services,name="view_services"),
    path("view_single_service",views.view_single_service,name="view_single_service"),

    #***********************SCHEDULE**************************

    path("place_order/",views.place_order,name="place_order"),
    path("view_order",views.view_order,name="view_order"),
    path("order/",views.checkout,name="checkout"),
    path("view_order_history/",views.view_order_history,name="view_order_history"),

    

#***********************MESSAGE**************************

    path("contact/", views.contact, name="send_message"),

#************************************PAYMENT**************************************** 

    path("create_payment_intent/",views.create_payment_intent,name="create_payment_intent"),
    path("stripe_webhook/",views.stripe_webhook,name="stripe_webhook")


]