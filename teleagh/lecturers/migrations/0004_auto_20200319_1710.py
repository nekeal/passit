# Generated by Django 2.2.6 on 2020-03-19 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecturers', '0003_auto_20200311_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='consultations',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='contact',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
