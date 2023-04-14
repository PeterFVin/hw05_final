from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    description = models.TextField('описание')
    slug = models.SlugField('ссылка', unique=True)
    title = models.CharField('название', max_length=200)

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    text = models.TextField(
        'текст поста',
        help_text='введите текст поста',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='группа',
        help_text='группа, к которой будет относиться пост',
    )
    image = models.ImageField(
        'картинка',
        upload_to='posts/',
        blank=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self) -> str:
        return self.text[: settings.NAME_STRING_LIMIT]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='комментарий',
    )
    text = models.TextField(
        'текст комментария',
        help_text='введите текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор',
    )
    created = models.DateTimeField('дата комментария', auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='фолловер',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор',
    )
