# Generated by Django 2.2.6 on 2020-04-02 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecturers', '0004_auto_20200319_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='title',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
