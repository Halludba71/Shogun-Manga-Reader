# Generated by Django 3.2.5 on 2022-03-18 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_remove_manga_nextchapter'),
    ]

    operations = [
        migrations.CreateModel(
            name='mangaCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryid', models.IntegerField()),
                ('mangaid', models.IntegerField()),
            ],
        ),
    ]
