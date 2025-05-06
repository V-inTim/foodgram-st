from django.db import models
from django.conf import settings


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_subscribe'
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f'{self.followed_user} - {self.user}'
