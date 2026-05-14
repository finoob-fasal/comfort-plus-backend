from urllib import request
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from AdminApp.models import Item_Price, Services, Staff
from UserApp.models import Service_Booking
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# ..............Admin_login...........
@api_view(['POST'])
def admin_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    
    
    if user is None:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_superuser:
        return Response({"error": "Access denied. Admins only."}, status=status.HTTP_403_FORBIDDEN)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "is_admin": True,
        "username": user.username
    })

# ............service.................
@api_view(["POST"])
def add_service(request):
    service_nme = request.data.get("s_name")
    desc = request.data.get("discription")
    s_price = request.data.get("s_prc")
    estimated_t = request.data.get("est_time")
    available = request.data.get("is_available") == "True"
    features = request.data.get("feature")


    if not service_nme or not s_price:
        return HttpResponse("its a mandatory field", status=400)

    try:
        Services.objects.create(
            service_type=service_nme,
            description=desc,
            price=s_price,
            estimated_time=estimated_t,
            is_available=available,
            features=features,
        )
        return HttpResponse("create successfully", status=201)
    except Exception as e:
        return HttpResponse(str(e), status=500)


@api_view(["GET"])
def view_services(request):
    services = Services.objects.all()
    new_list = []

    for i in services:
        new_list.append(
            {
                "id": i.id,
                "s_nme": i.service_type,
                "disc": i.description,
                "pr": i.price,
                "estimated_t": i.estimated_time,
                "is_avail": i.is_available,
                "cr_at": i.created_at,
                "up_st": i.updated_at,
                "ftr":i.features
            }
        )
    return JsonResponse(new_list, safe=False)


@api_view(["GET"])
def v_single_services(request, id):
    data = get_object_or_404(Services, id=id)
    service = {
        "id": data.id,
        "s_nme": data.service_type,
        "disc": data.description,
        "pr": data.price,
        "estimated_t": data.estimated_time,
        "is_avail": data.is_available,
        "cr_at": data.created_at,
        "up_st": data.updated_at,
        "ftr":data.features
    }
    return JsonResponse(service)


@csrf_exempt
def edit_service(request, id):
    if request.method == "GET":
        s_data = Services.objects.get(id=id)
        single_data = {
            "id": s_data.id,
            "s_nme": s_data.service_type,
            "disc": s_data.description,
            "pr": s_data.price,
            "estimated_t": s_data.estimated_time,
            "is_avail": s_data.is_available,
            "cr_at": s_data.created_at,
            "up_st": s_data.updated_at,
            "ftr":s_data.features
        }
        return JsonResponse(single_data)

    elif request.method == "PUT":
        body = json.loads(request.body)

        s_data = Services.objects.get(id=id)
        s_data.service_type = body.get("s_nme", s_data.service_type)
        s_data.description = body.get("disc", s_data.description)
        s_data.price = body.get("s_pr", s_data.price)
        s_data.estimated_time = body.get("est_t", s_data.estimated_time)
        s_data.is_available = body.get("is_avl", s_data.is_available)
        s_data.updated_at = body.get("up_at", s_data.updated_at)
        s_data.features = body.get("ftr", s_data.features)
        s_data.save()
        return HttpResponse("updated successfully", status=201)

    return JsonResponse("completed")


@api_view(["DELETE"])
def delete_service(request, id):
    data = Services.objects.get(id=id)
    data.delete()
    return JsonResponse({"message": "successfully deleted"})


# .....................view user..........................
@api_view(["GET"])
def view_users(request):
    signup_users = User.objects.filter(is_superuser=False, is_staff=False)
    users = []

    for user in signup_users:
        users.append(
            {
                "id": user.id,
                "Name": user.username,
                "Email": user.email,
                "Phone": user.profile.Phone if hasattr(user, "profile") else None,
            }
        )
    return JsonResponse(users, safe=False)


# ..................view order...................
@api_view(["GET"])
def view_orders(request):
    schedule = Service_Booking.objects.filter()
    data = []
    for i in schedule:
        data.append(
            {
                "full_name": i.full_name,
                "phone": i.phone,
                "email": i.email,
                "street_address": i.street_address,
                "city": i.city,
                "zipcode": i.zipcode,
                "service": i.service,
                "date": i.date,
                "time": i.time,
            }
        )
    return JsonResponse(data, safe=False)


@api_view(["GET"])
def view_user_orders(request, id):
    orders = Service_Booking.objects.filter(user_id = id)
    data = []
    for i in orders:
        data.append(
            {
                "full_name": i.full_name,
                "phone": i.phone,
                "email": i.email,
                "street_address": i.street_address,
                "city": i.city,
                "zipcode": i.zipcode,
                "service": i.service,
                "date": i.date,
                "time": i.time,
            }
        )
    return JsonResponse(data, safe=False)

@api_view(["GET"])
def view_user_order(request, id):
    orders = get_object_or_404(Service_Booking, id=id)
    data = {
        "full_name": orders.full_name,
        "phone": orders.phone,
        "email": orders.email,
        "street_address": orders.street_address,
        "city": orders.city,
        "zipcode": orders.zipcode,
        "service": orders.service,
        "date": orders.date,
        "time": orders.time,
    }
    return JsonResponse(data, safe=False)
# ................... Staff Recruiting ..................
@api_view(['POST'])
def add_staff(request):
    try:
        data = request.data

        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        role = data.get('role')

        if not name or not phone or not email or not role:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        if Staff.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        Staff.objects.create(
            name=name,
            phone=phone,
            email=email,
            role=role
        )

        return JsonResponse({'message': 'Added successfully'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@api_view(['GET'])
def view_all_staff(request):
    all_staff = Staff.objects.all()
    staff = []

    for i in all_staff:
        staff.append({
            'id': i.id,
            'name': i.name,
            'phone': i.phone,
            'email': i.email,
            'role': i.role,
            'status':i.status
        })
    return JsonResponse(staff, safe=False)


@api_view(['GET'])
def view_single_staff(request, id):
    data = Staff.objects.get(id=id)
    single_staff = ({
            'name': data.name,
            'phone': data.phone,
            'email': data.email,
            'role': data.role
        })
    return JsonResponse(single_staff)

@api_view(['DELETE'])
def remove_staff(request, id):
    data = Staff.objects.get(id=id)
    data.delete()
    return JsonResponse({'message':'successfully removed'})


@csrf_exempt
def edit_staff(request, id):
    if request.method == "GET":
        data = Staff.objects.get(id=id)
        single_data = {
            'name': data.name,
            'phone': data.phone,
            'email': data.email,
            'role': data.role,
            'status': data.status
        }
        return JsonResponse(single_data)

    elif request.method == "PUT":

        body = json.loads(request.body)

        data = Staff.objects.get(id=id)
        data.name = body.get("name", data.name)
        data.phone = body.get("phone", data.phone)
        data.email = body.get("email", data.email)
        data.role = body.get("role", data.role)
        data.status = body.get("status", data.status)
        data.save()
        return HttpResponse("updated successfully", status=201)

    return JsonResponse("completed")

# ..................items to service.................
@api_view(['POST'])
def add_item(request, id):
    item = request.data.get("item")
    price = request.data.get("price")

    print("Received:", item, price, id)

    if not item or not price:
        return HttpResponse("its a mandatory field", status=400)

    try:
        Item_Price.objects.create(
            service_id = id,
            item = item,
            price = price,
        )
        return HttpResponse("create successfully", status=201)
    except Exception as e:
        print("DB Error:", e)
        return HttpResponse(str(e), status=500)
    

@api_view(['GET'])
def view_items(request):
    items = Item_Price.objects.all().order_by('id')
    new_list = []

    for i in items:
        new_list.append(
            {
                'id': i.id,
                'item': i.item,
                'price': i.price,
                's_id': i.service.id,
                'service_name': i.service.service_type,
            }
        )
    return JsonResponse(new_list, safe=False)


@api_view(['GET'])
def view_single_item(request, id):
    data = get_object_or_404(Item_Price, id=id)

    item = {
        'item': data.item,
        'price': data.price,
        's_id': data.service.id
        }
    return JsonResponse(item)

@csrf_exempt
def edit_service_item(request, id):
    if request.method == 'GET':
        data = Item_Price.objects.get(id=id)
        single_data = {
            'item': data.item,
            'price': data.price,
            's_id': data.service.id
        }
        return JsonResponse(single_data)
    
    elif request.method == 'PUT':
        body = json.loads(request.body)

        data = Item_Price.objects.get(id=id)
        data.item = body.get('item', data.item)
        data.price = body.get('price', data.price)
        data.service_id = body.get('s_id', data.service_id)
        data.save()
        return HttpResponse("updated successfully", status=201)
    return JsonResponse('completed')


@api_view(['DELETE'])
def delete_service_item(request, id):
    data = Item_Price.objects.get(id=id)
    data.delete()
    return JsonResponse({"message": "successfully deleted"})