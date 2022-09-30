# Generated by Django 3.2.13 on 2022-09-28 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simple_recipes', '0005_alter_articlepicture_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentOf', to='simple_recipes.article')),
                ('commentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simple_recipes.profile')),
            ],
        ),
    ]