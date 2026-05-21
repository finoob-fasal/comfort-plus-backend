# from django.db import models
# from django.contrib.auth.models import User

# # Create your models here.


# class Profile(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     Phone=models.IntegerField()

# class Service_Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=15)
#     email = models.EmailField()
#     street_address = models.TextField()
#     city = models.CharField(max_length=100)
#     zipcode = models.CharField(max_length=10)
#     service = models.CharField(max_length=100)
#     date = models.DateField()
#     time = models.TimeField()
#     category=models.TextField(default="null")



# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     email = models.EmailField()
#     subject = models.CharField(max_length=200)
#     message = models.TextField()



from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)

# class Service_Booking(models.Model):

    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # full_name = models.CharField(max_length=100)
    # phone = models.CharField(max_length=15)
    # email = models.EmailField()
    # street_address = models.TextField()
    # city = models.CharField(max_length=100)
    # zipcode = models.CharField(max_length=10)
    # service = models.CharField(max_length=100)
    # size = models.CharField(max_length=20, choices=[
    #         ('small', 'Small'),
    #         ('large', 'Large'),
    #         ('others', 'Others')
    #     ],
    #     default='small'
    # )
    # date = models.DateField()
    # time = models.CharField(max_length=50)
    # Delivery_mode = models.CharField(max_length=10, choices=[('Normal', 'Normal'), ('Express', 'Express')],
    #     default='Normal'
    # )
    # order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

class Service_Booking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    date = models.DateField()
    time = models.CharField(max_length=100)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

class Message(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=200, default='')
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

class Order(models.Model):

    checkout = models.ForeignKey(
        Service_Booking,
        to_field="order_id",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    real_amount=models.IntegerField()
    BAG_CHOICES = [
        ('small', 'Small Bag'),
        ('large', 'Large Bag'),
    ]

    DELIVERY_CHOICES = [
        ('normal', 'Normal Delivery'),
        ('express', 'Express Delivery'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    Bag_type = models.CharField(
        max_length=20,
        choices=BAG_CHOICES
    )

    quantity = models.PositiveIntegerField(default=1)

    Delivery_Type = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES
    )

    

    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )


    # def __str__(self):
    #     return f"Order #{self.id} - {self.user} - {self.status}"
    
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # amount = models.IntegerField()

    # # ✅ Stripe fields
    # stripe_payment_intent = models.CharField(max_length=255, null=True, blank=True)

    # status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    # created_at = models.DateTimeField(auto_now_add=True)
    