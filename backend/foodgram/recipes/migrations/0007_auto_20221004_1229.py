# Generated by Django 2.2.16 on 2022-10-04 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20221004_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.IntegerField(verbose_name='Количество'),
        ),
    ]
