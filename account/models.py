from django.db import models 
from django.contrib.auth.models import AbstractUser , BaseUserManager, AbstractBaseUser
import uuid
from base.models import BaseModel
from datetime import timedelta, datetime
from shop.settings import EMAIL_EXPIRE_TIME, PHONE_EXPIRE_TIME
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
# Create your models here.

NEW, CODE_VERIFY, DONE, PHOTO_DONE = ('new', 'code_verify', 'done','photo_done')

VIA_PHONE, VIA_EMAIL = ('via_phone', 'via_email')
SELLER, CUSTOMER =('Seller', 'Customer')

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
        (SELLER, SELLER),
        (CUSTOMER, CUSTOMER)

    )
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    auth_status = models.CharField(max_length=20, choices=AUTH_STATUS, default =NEW)
    auth_type = models.CharField(max_length=120, choices=AUTH_TYPE)
    auth_role = models.CharField(max_length=20, choices=AUTH_ROLE)
    image = models.ImageField(upload_to='user/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
    
    def check_username(self):
        if not self.username:
            ud = str(uuid.uuid4())
            temp_username = f"username{ud[ud.rfind('_'):]}"

            while CustomUser.objects.filter(username=temp_username).exists():
                temp_username += random.randint(0,10)

            self.username = temp_username

    def check_pass(self):
        if not self.password:
            ud = str(uuid.uuid4())
            temp_password = f"password{ud[ud.rfind('_'):]}"
            self.password = temp_password
    
    def hashing_pass(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def email_normalize(self):
        if self.email:
            temp_email = self.email.lower()
            self.email = temp_email

    def token(self):
        refresh = RefreshToken.for_user(self)

        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
    def generate_code(self, verify_type):
        code = random.randint(1000,9999)

        Verify.objects.create(
            code=code,
            user=self,
            verify_type=verify_type
        )
    
    def save(self, *args, **kwargs):
        self.check_username()
        self.check_pass()
        self.hashing_pass()
        self.email_normalize()
        super().save(*args, **kwargs)
        



class Verify(BaseModel):
    VERIFY_TYPE = (
            (VIA_EMAIL, VIA_EMAIL),
            (VIA_PHONE, VIA_PHONE)
    )

    verify_type = models.CharField(max_length=20, choices=VERIFY_TYPE)
    used = models.BooleanField(default=False)
    expire_time = models.DateTimeField()
    code = models.CharField(max_length=4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='codes')

    def __str__(self):
        return f"{self.user.username}----{self.code}"
    
    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:
            self.expire_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRE_TIME)
        else:
            self.expire_time = datetime.now() +timedelta(minutes=PHONE_EXPIRE_TIME)
        super().save(*args, **kwargs)
    


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, username, password):
        if not email:
            raise ValueError("Email kiritilishi shart")
        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, username, password):
        user = self.create_user(email, phone_number, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=13, unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Verify(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='verifies')
    code = models.CharField(max_length=6)
    used = models.BooleanField(default=False)
    expiration_time = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.expiration_time:
            self.expiration_time = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.code}"


  







