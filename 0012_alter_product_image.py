# Generated by Django 3.2 on 2021-04-29 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art_shop', '0011_auto_20210426_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='art_shop/images'),
        ),
    ]
