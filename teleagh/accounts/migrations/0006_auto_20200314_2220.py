# Generated by Django 2.2.6 on 2020-03-14 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0008_auto_20200311_1339'),
        ('accounts', '0005_auto_20200308_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('profile', 'field_age_group')},
        ),
    ]
