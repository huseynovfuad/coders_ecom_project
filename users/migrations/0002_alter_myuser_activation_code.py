# Generated by Django 3.2 on 2023-03-01 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='activation_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
