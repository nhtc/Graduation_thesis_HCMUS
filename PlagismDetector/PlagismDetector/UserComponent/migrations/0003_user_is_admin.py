# Generated by Django 3.1.4 on 2021-03-16 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserComponent', '0002_auto_20210317_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
