# Generated by Django 4.2 on 2023-08-04 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='producto', verbose_name='Imagen 1'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='producto', verbose_name='Imagen 2'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='producto', verbose_name='Imagen 3'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='producto', verbose_name='Imagen 4'),
        ),
    ]
