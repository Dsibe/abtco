# Generated by Django 2.2.13 on 2020-10-20 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('text', models.CharField(max_length=1500)),
                ('name', models.CharField(max_length=150)),
                ('location', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
    ]
