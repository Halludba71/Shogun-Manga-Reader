# Generated by Django 3.2.5 on 2022-03-17 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_manga_lastread'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manga',
            old_name='lastRead',
            new_name='nextChapter',
        ),
    ]
