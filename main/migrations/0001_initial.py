# Generated by Django 2.2.2 on 2019-07-29 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dates', models.CharField(blank=True, max_length=10000, null=True)),
            ],
        ),
    ]
