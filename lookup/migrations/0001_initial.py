# Generated by Django 2.0.4 on 2018-04-11 16:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_id', models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator(code='invalid short_id', message='short_id must be Alphanumeric', regex='^[a-zA-Z0-9]*$')])),
                ('description', models.CharField(blank=True, max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('method', models.CharField(choices=[('GET', 'GET'), ('POST', 'POST')], max_length=5)),
                ('paramtype', models.CharField(choices=[('COOKIE', 'cookie'), ('QUERY', 'query string'), ('HEADER', 'HTTP Header')], max_length=10)),
                ('paramname', models.CharField(max_length=100)),
            ],
        ),
    ]