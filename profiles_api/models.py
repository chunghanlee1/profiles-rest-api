from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class  UserProfileManager(BaseUserManager):
    """Manager for user profiles when we use the django command line tool"""
    def create_user(self, email, name, password=None):
        """New User profile"""
        if not email:
            raise ValueError('Users must have email address')
        #need to normalize (i.e. make second half of email address all lower case for case insensitivity)
        email=self.normalize_email(email)
        user=self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, name, password):
        """Create and save new superuser"""
        user=self.create_user(email,name,password)
        user.is_superuser=True #built-in in Permissions mixin
        user.is_staff=True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email=models.EmailField(max_length=225, unique=True)
    name=models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    #for managing users
    objects= UserProfileManager()

    #Override the normal username field with email
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']

    #Let django interact with custom user model. Override default methods
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        return self.email



from django.conf import settings#In order to retrieve the AUTH_USER_MODEL
class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile=models.ForeignKey(
        settings.AUTH_USER_MODEL,#Flexible reference in case we want to switch back to normal auth models in the future
        on_delete=models.CASCADE
    )
    status_text=models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.status_text