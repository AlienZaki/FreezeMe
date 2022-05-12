# Generated by Django 3.2.13 on 2022-05-12 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20220511_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='finished',
            field=models.BooleanField(choices=[(True, 'Finished'), (False, 'Pending')], default=False),
        ),
    ]
