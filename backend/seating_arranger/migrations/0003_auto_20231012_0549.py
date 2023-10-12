# Generated by Django 3.2.12 on 2023-10-12 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seating_arranger', '0002_classcsv_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomno', models.IntegerField()),
                ('rows', models.IntegerField()),
                ('columns', models.IntegerField()),
                ('noofbenches', models.IntegerField()),
                ('benchstrength', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='classCsv',
        ),
    ]
