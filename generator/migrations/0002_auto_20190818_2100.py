# Generated by Django 2.0.13 on 2019-08-18 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='law',
            name='law_name',
            field=models.TextField(),
        ),
    ]
