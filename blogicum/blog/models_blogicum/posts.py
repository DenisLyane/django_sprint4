from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .category import Category
from .location import Location
from .publishedmodel import PublishedModel
from .users import User


class PostQuerySet(models.QuerySet):

    def published(self):
        return super().filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )

    def commen_count(self):
        return self.annotate(
            comment_count=models.Count('comments')
        ).order_by('-pub_date')


class PublishedPostManager(models.Manager):

    def get_queryset(self):
        return (
            PostQuerySet(self.model, using=self._db).published()
        )

    def commen_count(self):
        return self.get_queryset().commen_count()


class Post(PublishedModel):
    title = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем —'
            ' можно делать отложенные публикации.'
        )
    )
    image = models.ImageField(
        'Фото',
        upload_to='posts_images',
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )

    objects = PostQuerySet.as_manager()
    published = PublishedPostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})

    def __str__(self):
        return self.title
