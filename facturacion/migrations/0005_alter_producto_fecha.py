# Generated by Django 4.2 on 2024-08-19 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0004_alter_producto_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='fecha',
            field=models.DateField(auto_now=True),
        ),
    ]