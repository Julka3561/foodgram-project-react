# Generated by Django 2.2.16 on 2022-10-04 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_tag_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='test',
            field=models.PositiveSmallIntegerField(verbose_name='Время приготовления (в минутах)'),
        ),
    ]