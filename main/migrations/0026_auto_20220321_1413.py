# Generated by Django 3.2.5 on 2022-03-21 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_download_downloaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='name',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='download',
            name='totalPages',
            field=models.IntegerField(default=0),
        ),
    ]
