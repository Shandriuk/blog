# Generated by Django 3.2.5 on 2021-07-21 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='blog_author',
            new_name='user',
        ),
    ]