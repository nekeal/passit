# Generated by Django 2.2.6 on 2020-03-11 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subject", "0007_resource_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subjectofagegroup",
            name="lecturers",
            field=models.ManyToManyField(
                related_name="subject_groups",
                through="lecturers.LecturerOfSubject",
                to="lecturers.Lecturer",
            ),
        ),
    ]
