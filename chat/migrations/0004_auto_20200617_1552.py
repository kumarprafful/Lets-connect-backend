# Generated by Django 3.0.7 on 2020-06-17 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20200614_1609'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-created_at']},
        ),
    ]