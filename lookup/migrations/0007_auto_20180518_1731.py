# Generated by Django 2.0.4 on 2018-05-18 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0006_auto_20180507_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lookup',
            name='extraparams',
            field=models.CharField(blank=True, help_text='Extra querystring parameters in comma-separated name:value pairs', max_length=200, null=True),
        ),
    ]