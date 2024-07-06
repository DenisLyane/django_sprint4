from django.conf import settings
from django.db import models

from .publishedmodel import PublishedModel


class Category(PublishedModel):
    title = models.CharField(
        max_length=settings.MAX_LENGTH,
        blank=True,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        blank=True,
        help_text=(
            'Идентификатор страницы для URL;'
            ' разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title
