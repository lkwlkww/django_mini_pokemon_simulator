# Generated by Django 4.0.3 on 2022-03-28 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0003_remove_pokemon_level_remove_pokemon_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='captured',
            field=models.BooleanField(default=False),
        ),
    ]