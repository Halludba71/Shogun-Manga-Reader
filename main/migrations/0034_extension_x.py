# Generated by Django 3.2.5 on 2022-03-30 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_delete_sources'),
    ]

    operations = [
        migrations.AddField(
            model_name='extension',
            name='x',
            field=models.IntegerField(default=2),
        ),
    ]