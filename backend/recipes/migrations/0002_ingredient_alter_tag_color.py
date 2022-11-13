# Generated by Django 4.1.3 on 2022-11-13 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, unique=True, verbose_name='Ингредиент')),
                ('measurement_unit', models.CharField(max_length=254, verbose_name='Еденица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(choices=[('#0000FF', 'Синий'), ('#008000', 'Зелёный'), ('#FF0000', 'Красный'), ('#FFCA86', 'Оранжевый'), ('#ffffff', 'Белый'), ('#FFFF00', 'Жёлтый')], max_length=254, unique=True, verbose_name='Цвет тэга'),
        ),
    ]
