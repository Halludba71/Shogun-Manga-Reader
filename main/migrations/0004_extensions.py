# Generated by Django 3.2.4 on 2021-10-18 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_manga_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='extensions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, default='')),
                ('location', models.TextField(blank=True, default='')),
            ],
        ),
    ]