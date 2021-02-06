from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,password=None):
        if not email:
            raise ValueError("user must have an email")
        email=email.lower()
        first_name=first_name.title()
        last_name=last_name.title()
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name, last_name, password=None):
        user=self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_superuser=True
        user.is_staff=True
        user.is_active=True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True,verbose_name='Email')
    first_name = models.CharField(max_length=20,verbose_name='First Name')
    last_name = models.CharField(max_length=20,verbose_name='Last Name')
    city = models.CharField(max_length=20,verbose_name='City Name')
    register_free= models.FloatField(default=0.0)
    purpose = models.TextField(max_length=200,blank=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name','last_name')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_varified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def get_short_name(self):
        return self.email
    def has_perm(self,prem,obj=None):
        return self.is_superuser
    def has_module_perms(self,app_label):
        return self.is_superuser
    def title_name(self):
        return self.first_name
    class Meta:
        verbose_name_plural='users'
