# Generated by Django 3.2.13 on 2022-09-28 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_recipes', '0007_articlecomment_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlecomment',
            options={'ordering': ['-date']},
        ),
    ]