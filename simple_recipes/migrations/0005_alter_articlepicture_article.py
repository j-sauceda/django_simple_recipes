# Generated by Django 3.2.13 on 2022-09-28 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simple_recipes', '0004_article_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepicture',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictureOf', to='simple_recipes.article'),
        ),
    ]
