# Generated by Django 3.2.5 on 2022-03-16 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_extension_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='url',
            field=models.TextField(default=''),
        ),
    ]
