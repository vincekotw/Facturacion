# Generated by Django 4.2 on 2024-10-23 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogo',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, default="2024-10-23 01:14"),
            preserve_default=False,
        ),
    ]
