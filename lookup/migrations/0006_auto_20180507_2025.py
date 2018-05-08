# Generated by Django 2.0.4 on 2018-05-07 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0005_jwksuri'),
    ]

    operations = [
        migrations.AddField(
            model_name='jwksuri',
            name='hint',
            field=models.CharField(blank=True, help_text='if a JWT token is expected to match some parameter in the JWKS to better match tokens to URIs', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='jwksuri',
            name='URL',
            field=models.URLField(default='test', help_text='JWKS URI', unique=True),
            preserve_default=False,
        ),
    ]
