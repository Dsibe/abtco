# Generated by Django 2.2.18 on 2021-07-11 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210710_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, default='51211262139107143386f9d-5269-43da-b5c7-f3a7852f1f7f2021-07-11-161053971422', max_length=400, null=True, unique=True),
        ),
    ]