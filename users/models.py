from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Custom related name to avoid conflict
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Custom related name to avoid conflict
        blank=True,
    )

User = get_user_model()

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"FriendRequest from {self.from_user.username} to {self.to_user.username}"