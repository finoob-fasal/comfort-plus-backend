# from django.urls import path
# from UserApp import views

# urlpatterns = [
    
#     path("signup/", views.user_signup, name="user_signup"),
#     path("login/", views.user_login, name="user_login"),

#     #*********************PROFILE***********************

#     path("view_profile",views.view_profile,name="view_profile"),
#     path("update_profile",views.update_profile,name="update_profile"),

#     #*********************SERVICES***********************

#     path("view_services",views.view_services,name="view_services"),
#     path("view_single_service",views.view_single_service,name="view_single_service"),


#     #***********************SCHEDULE**************************

#     path("place_order",views.place_order,name="place_order"),
#     path("view_order",views.view_order,name="view_order"),

# #***********************MESSAGE**************************

#     path("send_message",views.send_message,name="send_message"),
    
# ]




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

#***********************MESSAGE**************************

    path("contact/", views.contact, name="send_message"),

#************************************PAYMENT**************************************** 

    path("create_payment_intent/",views.create_payment_intent,name="create_payment_intent"),
    path("stripe_webhook/",views.stripe_webhook,name="stripe_webhook")


#*************************RESET PASSWORD****************************
    # path("reset_password",views.reset_password,name="reset_password"),



    
]