# Generated by Django 2.2 on 2019-04-15 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ga', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logical',
            old_name='logical_thinking_score',
            new_name='logical_score',
        ),
        migrations.AddField(
            model_name='logical',
            name='game_id',
            field=models.IntegerField(default=0),
        ),
    ]
