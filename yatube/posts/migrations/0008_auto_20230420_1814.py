# Generated by Django 2.2.16 on 2023-04-20 15:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0007_auto_20230419_2311'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='posts_follow_prevent_self_follow',
        ),
    ]
