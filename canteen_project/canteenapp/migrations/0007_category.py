# Generated by Django 5.1.6 on 2025-02-25 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteenapp', '0006_remove_fooditems_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
