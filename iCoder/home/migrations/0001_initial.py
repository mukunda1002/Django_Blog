# Generated by Django 4.2.4 on 2023-08-28 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=12)),
                ('email', models.CharField(max_length=50)),
                ('content', models.TextField()),
            ],
        ),
    ]
