# Generated by Django 2.2.6 on 2020-02-20 20:39
import django.db.models.deletion
from django.db import migrations, models

from ...subject.models import FieldOfStudy, FieldOfStudyOfAgeGroup


def get_default_field_age_group():
    default_field_of_study, _ = FieldOfStudy.objects.get_or_create(
        name="default field", slug="default-field"
    )
    default_field_age_group, _ = FieldOfStudyOfAgeGroup.objects.get_or_create(
        field_of_study=default_field_of_study, students_start_year=2000
    )
    return default_field_age_group.id


class Migration(migrations.Migration):

    dependencies = [
        ("subject", "0004_auto_20200210_1518"),
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="field_age_group",
            field=models.ForeignKey(
                default=get_default_field_age_group,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="news",
                to="subject.FieldOfStudyOfAgeGroup",
            ),
            preserve_default=False,
        ),
    ]
