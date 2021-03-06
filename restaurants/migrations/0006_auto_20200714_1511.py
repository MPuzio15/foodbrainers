# Generated by Django 3.0.7 on 2020-07-14 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_auto_20200714_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='menu',
        ),
        migrations.AlterField(
            model_name='course',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='menu', to='restaurants.Restaurant'),
        ),
    ]
