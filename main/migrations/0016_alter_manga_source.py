# Generated by Django 3.2.4 on 2022-03-16 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_manga_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='source',
            field=models.IntegerField(),
        ),
    ]