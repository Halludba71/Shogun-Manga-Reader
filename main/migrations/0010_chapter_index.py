# Generated by Django 3.2.4 on 2022-02-11 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_chapter_comicid'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='index',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
