# Generated by Django 2.2.6 on 2020-03-20 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20200319_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='attachment',
            field=models.FileField(blank=True, upload_to='attachments'),
        ),
    ]
