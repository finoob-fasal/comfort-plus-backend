# from urllib import request

# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.authtoken.models import Token
# from django.http import HttpResponse, JsonResponse
# from django.contrib.auth.models import User
# from UserApp.models import  Profile,Service_Booking,Message
# from rest_framework.decorators import permission_classes,api_view
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import authenticate,login
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.core.exceptions import ObjectDoesNotExist
# from AdminApp.models import Services

# # Create your views here.

# @csrf_exempt
# def user_signup(request):
#     if request.method=='POST':
#         rname=request.POST.get("name")
#         rmail=request.POST.get("mail")
#         rphone=request.POST.get("phone")
#         rpass=request.POST.get("pass")
#         if not rmail or not rphone:
#             return HttpResponse("This field is mandatory")
        

#         if User.objects.filter(email=rmail).exists():
#            return HttpResponse("Email already exists")
        

#         user=User.objects.create_user(
#             username=rname,
#             email=rmail, 
#             password=rpass
#         )
#         Profile.objects.create(
#             user=user,
#             Phone=rphone
#         )
#         return JsonResponse({'message': 'successfully created'})

#     return JsonResponse({'message': 'invalid request'})


# @csrf_exempt
# def user_login(request):
#     if request.method == "POST":

#         email = request.POST.get("mail")
#         password = request.POST.get("pass")

#         if not email or not password:
#             return JsonResponse({"message": "Email and password required"})

#         try:
#             user_obj = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return JsonResponse({"message": "Invalid credentials"})

#         user = authenticate(username=user_obj.username, password=password)

#         if user is None:
#             return JsonResponse({"message": "Invalid credentials"})

#         # session login
#         login(request, user)

#         # JWT tokens
#         refresh = RefreshToken.for_user(user)

#         return JsonResponse({
#             "message": "Login successful",
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#             "user": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email
#             }
#         })

#     return JsonResponse({"message": "Invalid request"})




# #*****************************PROFILE*******************************

# #VIEW PROFILE

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def view_profile(request):
#     user = request.user
#     try:
#         profile = user.profile
#         phone = profile.Phone
#     except ObjectDoesNotExist:
#         phone = None

#     data = {
#         "name": user.username,
#         "mail": user.email,
#         "phone": phone
#     }

#     return JsonResponse(data)

# #UPDATE PROFILE

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def update_profile(request):
#     user = request.user

#     # Ensure profile exists
#     try:
#         profile = user.profile
#     except ObjectDoesNotExist:
#         # Optionally, create profile if missing
#         profile = Profile.objects.create(user=user)

#     # Update username
#     user.username = request.data.get("name", user.username)

#     # Update email safely
#     new_email = request.data.get("email", user.email)
#     if User.objects.filter(email=new_email).exclude(id=user.id).exists():
#         return JsonResponse({"message": "Email already exists"}, status=400)
#     user.email = new_email
#     user.save()

#     # Update phone
#     profile.Phone = request.data.get("phone", profile.Phone)
#     profile.save()

#     return JsonResponse({"message": "Updated successfully"})





# #****************************SERVICE****************************

# #*VIEW_SERVICES

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def view_services(request):
#     services = Services.objects.all()
#     new_list = []

#     for i in services:
#         new_list.append({
#             "id": i.id,
#             "s_nme": i.service_type,
#             "disc": i.description,
#             "price": i.price,
#             "estimated_t": i.estimated_time,
#             "is_avail": i.is_available,
#             "cr_at": i.created_at,
#             "up_st": i.updated_at
#         })
#     return JsonResponse(new_list, safe=False)

# #VIEW_SINGLE_SERVICE

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def view_single_service(request,id):
#     service = Services.objects.get(id=id)

#     data = {
#         "id": service.id,
#         "s_nme": service.service_type,
#         "disc": service.description,
#         "price": service.price,
#         "estimated_t": service.estimated_time,
#         "is_avail": service.is_available,
#         "cr_at": service.created_at,
#         "up_st": service.updated_at
#     }

#     return JsonResponse(data)

# #*************************SCHEDEULE*****************************

# #SERVICE_BOOKING

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def place_order(request):

#     rfull_name = request.data.get("full_name")
#     rphone = request.data.get("phone")
#     rmail = request.data.get("email")
#     raddress = request.data.get("street_address")
#     rcity = request.data.get("city")
#     rzipcode = request.data.get("zipcode")
#     rservice_type = request.data.get("service")
#     rdate = request.data.get("date")
#     rtime = request.data.get("time")

#     Service_Booking.objects.create(
#         user=request.user,
#         full_name=rfull_name,
#         phone=rphone,
#         email=rmail,
#         street_address=raddress,
#         city=rcity,
#         zipcode=rzipcode,
#         service=rservice_type,
#         date=rdate,
#         time=rtime
#     )

#     return JsonResponse({"message": "Success"})

    
# #VIEW_ORDER

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def view_order(request):
#         schedule=Service_Booking.objects.filter(user=request.user)
#         data=[]
#         for i in schedule:
#             data.append(
#                 {
#                     "full_name":i.full_name,
#                     "phone":i.phone,
#                     "email":i.email,
#                     "street_address":i.street_address,
#                     "city":i.city,
#                     "zipcode":i.zipcode,
#                     "service":i.service,
#                     "date":i.date,
#                     "time":i.time
#                 }
#             )
#         return JsonResponse(data,safe=False)

# #******************MESSAGE***************

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def send_message(request):

#     rmail=request.POST.get("mail")
#     rsubject=request.POST.get("subject")
#     rmessage=request.POST.get("message")
#     if not rmail:
#         return HttpResponse("This is mandatory")
#     Message.objects.create(
#         user=request.user,
#         email=rmail,
#         subject=rsubject,
#         message=rmessage
#     )
#     return HttpResponse("Success")









import json
from urllib import request

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, JsonResponse
import stripe
from .models import Order, Order_payment, User
from UserApp.models import  Profile,Service_Booking,Message
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from AdminApp.models import Services
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from .models import Profile

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny

@api_view(['POST'])
# @permission_classes([AllowAny])
def user_signup(request):

    data = request.data

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    if not email or not phone or not password:
        return Response(
            {"message": "Required fields are missing"},
            status=400
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"message": "Email already exists"},
            status=400
        )

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name=name
    )
    

    Profile.objects.create(
        user=user,
        phone=phone
    )

    return Response({
        "message": "User created successfully"
    })
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response


from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.http import JsonResponse

@api_view(['POST'])
def user_login(request):

    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return JsonResponse(
            {"message": "Email and password required"},
            status=400
        )

    # get user by email
    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse(
            {"message": "Invalid credentials"},
            status=401
        )

    # authenticate using username + password
    user = authenticate(username=user_obj.username, password=password)

    if user is None:
        return JsonResponse(
            {"message": "Invalid credentials"},
            status=401
        )

    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    })

#**********PROFILE**********

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_profile(request):
    user = request.user
    profile = user.profile

    return Response({
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": profile.phone
    })

#UPDATE PROFILE

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    profile = user.profile   # 👈 IMPORTANT (OneToOne relation)

    print("DATA:", request.data)

    # ✅ Update User fields
    user.first_name = request.data.get("first_name", user.first_name)
    user.last_name = request.data.get("last_name", user.last_name)
    user.email = request.data.get("email", user.email)
    user.save()

    # ✅ Update Profile fields
    profile.phone = request.data.get("phone", profile.phone)
    profile.save()

    return Response({
        "message": "Profile updated successfully",
        "data": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": profile.phone
        }
    })



#*********SERVICE*********

#*VIEW_SERVICES

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_services(request):
    services = Services.objects.all()
    new_list = []

    for i in services:
        new_list.append({
            "id": i.id,
            "s_nme": i.service_type,
            "disc": i.description,
            "price": i.price,
            "estimated_t": i.estimated_time,
            "is_avail": i.is_available,
            "cr_at": i.created_at,
            "up_st": i.updated_at
        })
    return JsonResponse(new_list, safe=False)

#VIEW_SINGLE_SERVICE

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_single_service(request,id):
    service = Services.objects.get(id=id)

    data = {
        "id": service.id,
        "s_nme": service.service_type,
        "disc": service.description,
        "price": service.price,
        "estimated_t": service.estimated_time,
        "is_avail": service.is_available,
        "cr_at": service.created_at,
        "up_st": service.updated_at
    }

    return JsonResponse(data)

#********SCHEDEULE**********

#SERVICE_BOOKING


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def place_order(request):

    rfull_name = request.data.get("name")
    rphone = request.data.get("phone")
    rmail = request.data.get("email")
    raddress = request.data.get("street")
    rcity = request.data.get("city")
    rzipcode = request.data.get("zipcode")
    # rservice_type = request.data.get("service")
    # rsize = request.data.get("size")   # added size
    rdate = request.data.get("date")
    rtime = request.data.get("time")

    Service_Booking.objects.create(
        # user=request.user,
        user=None,
        full_name=rfull_name,
        phone=rphone,
        email=rmail,
        street_address=raddress,
        city=rcity,
        zipcode=rzipcode,
        # service=rservice_type,
        # size=rsize,          # added here
        date=rdate,
        time=rtime,
        # Delivery_mode="Normal"
    )

    return JsonResponse({"message": "Success"})

    
#VIEW_ORDER

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_order(request):
        schedule=Service_Booking.objects.filter(user=request.user)
        data=[]
        for i in schedule:
            data.append(
                {
                    "full_name":i.full_name,
                    "phone":i.phone,
                    "email":i.email,
                    "street_address":i.street_address,
                    "city":i.city,
                    "zipcode":i.zipcode,
                    "service":i.service,
                    "date":i.date,
                    "time":i.time
                }
            )
        return JsonResponse(data,safe=False)


@api_view(['POST'])
def checkout(request):

    bag_type = request.data.get("Bag_type")
    quantity = request.data.get("quantity")
    delivery_type = request.data.get("Delivery_Type")
    price_ord = request.data.get("price_ord")

    order = Order_payment.objects.create(
        user=request.user,
        Bag_type=bag_type,
        quantity=quantity,
        Delivery_Type=delivery_type,
        price_ord=price_ord
    )

    return Response({
        "message": "Checkout Success",
        "id": order.id,
        "Bag_type": order.Bag_type,
        "quantity": order.quantity,
        "Delivery_Type": order.Delivery_Type,
        "price_ord": order.price_ord
    })


# VIEW ORDER HISTORY

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_order_history(request):

    orders = Order_payment.objects.filter(user=request.user).order_by("-created_at")
    data = []

    for order in orders:
        data.append({
            "bag_type": order.Bag_type,
            "date": order.created_at,
            "price_ord": order.price_ord
        })

    return Response({
        "message": "Order history fetched successfully",
        "orders": data
    })

#*******MESSAGE******

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def contact(request):

    rname=request.data.get("name")
    rmail = request.data.get("email")
    rsubject = request.data.get("subject")
    rmessage = request.data.get("message")

    if not rmail:
        return HttpResponse("This is mandatory")

    Message.objects.create(
        # user=request.user,
        name=rname,
        email=rmail,
        subject=rsubject,
        message=rmessage
    )

    return HttpResponse("Success")

#RESET_PASSWORD

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def reset_password(request):

#     password=request.data.get("current password")
#     new_password=request.data.get("new_password")
#     confirm_password=request.data.get("confirm_password")
#     user = request.user
#     if not User.check_password(password):
#      return HttpResponse("Incorrect password")
#     if new_password != confirm_password:
#        return HttpResponse("Passwords do not match")
# # set new password
#     user.set_password(new_password)
#     user.save()
    # return JsonResponse({"message":"success"})

# .....................PAYMENT.........................
# views.py
import stripe
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_intent(request):

    try:

        bag_type = request.data.get("bag_type")
        count = int(request.data.get("count", 1))
        delivery_type = request.data.get("delivery_type")

        # Fixed rates
        SMALL_BAG_PRICE = 100
        LARGE_BAG_PRICE = 200

        EXPRESS_CHARGE = 50
        NORMAL_CHARGE = 0

        # Bag price
        if bag_type == "small":
            bag_price = SMALL_BAG_PRICE
        elif bag_type == "large":
            bag_price = LARGE_BAG_PRICE
        else:
            return Response({
                "error": "Invalid bag type"
            }, status=400)

        # Delivery charge
        if delivery_type == "express":
            delivery_charge = EXPRESS_CHARGE
        else:
            delivery_charge = NORMAL_CHARGE

        # Total calculation
        total_amount = (bag_price * count) + delivery_charge

        # Stripe uses paise
        stripe_amount = total_amount * 100

        print("Total:", total_amount)

        intent = stripe.PaymentIntent.create(
            amount=stripe_amount,
            currency="inr",
        )

        order = Order.objects.create(
            user=request.user,
            amount=total_amount,
            stripe_payment_intent=intent.id,
            status="PENDING"
        )

        return Response({
            "client_secret": intent.client_secret,
            "total_amount": total_amount
        })

    except Exception as e:

        print("STRIPE ERROR:", str(e))

        return Response({
            "error": str(e)
        }, status=500)
# import stripe
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import permission_classes
# from django.conf import settings
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Order

# stripe.api_key = settings.STRIPE_SECRET_KEY
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_payment_intent(request):

#     try:

#         amount = int(request.data.get("amount", 0))

#         amount = amount * 100

#         print("Amount:", amount)

#         intent = stripe.PaymentIntent.create(
#             amount=amount,
#             currency="inr",
#         )

#         print("Intent:", intent)

#         order = Order.objects.create(
#             user=request.user,
#             amount=amount,
#             stripe_payment_intent=intent.id,
#             status="PENDING"
#         )

#         return Response({
#             "client_secret": intent.client_secret
#         })

#     except Exception as e:

#         print("STRIPE ERROR:", str(e))

#         return Response({
#             "error": str(e)
#         }, status=500)

import stripe
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )

        print(event["type"])

    except Exception as e:
        print(e)
        return HttpResponse(status=400)

    return HttpResponse(status=200)















