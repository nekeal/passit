# Generated by Django 2.2.6 on 2020-02-29 21:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200229_1658'),
        ('news', '0002_news_field_age_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='created_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='news_created',
                to='accounts.UserProfile',
            ),
        ),
        migrations.AddField(
            model_name='news',
            name='modified_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='news_modified',
                to='accounts.UserProfile',
            ),
        ),
    ]
