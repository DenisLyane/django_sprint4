from django.conf import settings
from django.db import models

from .publishedmodel import PublishedModel


class Location(PublishedModel):
    name = models.CharField(
        max_length=settings.MAX_LENGTH,
        blank=True,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name
