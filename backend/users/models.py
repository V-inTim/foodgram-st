from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_subscribe'
    )
    followed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed_user_subscribe'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'followed_user'],
                name='unique_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.followed_user} - {self.user}'
