# Generated by Django 3.2.4 on 2022-02-11 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_chapter'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='comicId',
            field=models.IntegerField(default=9),
            preserve_default=False,
        ),
    ]