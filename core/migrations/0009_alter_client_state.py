# Generated by Django 3.2.13 on 2022-05-10 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('state', '0002_auto_20220510_1602'),
        ('core', '0008_delete_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='state.state'),
        ),
    ]
