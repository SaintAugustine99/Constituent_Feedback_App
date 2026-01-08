from django.contrib.auth.models import AbstractUser
from django.db import models
from locations.models import Ward

class User(AbstractUser):
    # We use 'User' instead of 'CustomUser' to keep it simple, 
    # but we will point AUTH_USER_MODEL to this.
    
    ward = models.ForeignKey(
        Ward, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='residents',
        help_text="The political ward where this user resides."
    )
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
