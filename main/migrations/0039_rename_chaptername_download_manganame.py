# Generated by Django 3.2.4 on 2022-03-31 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_download_chaptername'),
    ]

    operations = [
        migrations.RenameField(
            model_name='download',
            old_name='chapterName',
            new_name='mangaName',
        ),
    ]