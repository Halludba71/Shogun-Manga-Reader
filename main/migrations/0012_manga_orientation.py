# Generated by Django 3.2.4 on 2022-02-11 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_manga_chapters'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='orientation',
            field=models.TextField(default='left-to-right'),
        ),
    ]