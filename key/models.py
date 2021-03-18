from django.db import models
from core import models as core_models

import datetime
from django.utils import timezone
import uuid
# Create your models here.

class SecretMsg(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    message = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.message

    def was_published_recently(self):
        return self.pub_date >= timezone.now() -datetime.timedelta(days=1)
