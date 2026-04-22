from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel
from django.db import models
import uuid

class User(TimeStampedModel, AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True)
