# Generated by Django 3.2.13 on 2022-09-28 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_recipes', '0003_auto_20220928_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='body',
            field=models.TextField(null=True),
        ),
    ]
