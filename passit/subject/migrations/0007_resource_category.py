# Generated by Django 2.2.6 on 2020-03-09 20:00

from django.db import migrations, models

from passit.subject.models import ResourceCategoryChoices


class Migration(migrations.Migration):

    dependencies = [
        ("subject", "0006_auto_20200308_1821"),
    ]

    operations = [
        migrations.AddField(
            model_name="resource",
            name="category",
            field=models.CharField(
                choices=ResourceCategoryChoices.choices(),
                default=ResourceCategoryChoices.OTHER,
                max_length=50,
            ),
            preserve_default=False,
        ),
    ]
