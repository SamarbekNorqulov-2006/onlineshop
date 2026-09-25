from django.db import models
from django.contrib.auth.models import AbstractUser

from base.models import BaseModel
from datetime import timedelta, datetime
from shop.settings import EMAIL_EXPIRE_TIME, PHONE_EXPIRE_TIME
# Create your models here.

NEW, CODE_VERIFY, DONE, PHOTO_DONE = ('new', 'code_verify', 'done','photo_done')

VIA_PHONE, VIA_EMAIL = ('via_phone', 'via_email')
SELLER, CUSTOMER =('seller', 'customer')

class CustomUser(AbstractUser, BaseModel):
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFY, CODE_VERIFY),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE)
    )

    AUTH_TYPE = (
    
    (VIA_EMAIL, VIA_EMAIL),
    (VIA_PHONE, VIA_PHONE),
    )
    AUTH_ROLE =(
        (SELLER, SELLER)
        (CUSTOMER, CUSTOMER)

    )
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=13, unique=True, blank=True, null=True)
    auth_status = models.CharField(max_length=20, choices=AUTH_STATUS, default =True)
    auth_type = models.CharField(max_length=120, choices=AUTH_TYPE)
    auth_role = models.CharField(max_length=20, choices=AUTH_ROLE)
    image = models.ImageField(upload_to='user/', blank=True, null=True)
    address = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.username
    
class Verify(BaseModel):
    VERIFY_TYPE = (
            (VIA_EMAIL, VIA_EMAIL),
            (VIA_PHONE, VIA_PHONE)
    )

    verify_type = models.CharField(max_length=20, choices=VERIFY_TYPE)
    used = models.BooleanField(defauld=False)
    expire_time = models.DateTimeField()
    code = models.CharField(max_length=4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}----{self.code}"
    
    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:
            self.expire_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRE_TIME)
        else:
            self.expire_time = datetime.now() +timedelta(minutes=PHONE_EXPIRE_TIME)
        super().save(*args, **kwargs)
    
    
    




