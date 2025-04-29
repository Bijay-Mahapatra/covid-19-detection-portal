from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_expiry = models.DateTimeField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    class Meta:
        db_table = 'patients'

    def generate_reset_token(self):
        self.reset_token = str(uuid.uuid4())
        self.reset_token_expiry = timezone.now() + timezone.timedelta(hours=1)
        self.save()
        return self.reset_token

    def clear_reset_token(self):
        self.reset_token = None
        self.reset_token_expiry = None
        self.save()