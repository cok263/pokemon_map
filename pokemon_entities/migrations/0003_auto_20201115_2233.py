# Generated by Django 2.2.3 on 2020-11-15 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0002_auto_20201115_2224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemon',
            old_name='title_ru',
            new_name='title',
        ),
    ]
