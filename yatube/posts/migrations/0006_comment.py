# Generated by Django 2.2.16 on 2023-04-08 17:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'text',
                    models.TextField(
                        help_text='введите текст комментария',
                        verbose_name='текст комментария',
                    ),
                ),
                (
                    'created',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='дата комментария'
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='автор',
                    ),
                ),
                (
                    'post',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                        to='posts.Post',
                        verbose_name='комментарий',
                    ),
                ),
            ],
        ),
    ]
