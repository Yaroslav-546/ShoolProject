# Generated by Django 4.2.16 on 2024-11-05 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='active',
            field=models.CharField(choices=[('1active', '1 Кружок'), ('2active', '2 Кружок'), ('3active', '3 Кружок'), ('4active', '4 Кружок')], max_length=8),
        ),
    ]
