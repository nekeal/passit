# Generated by Django 2.2.6 on 2020-03-11 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("subject", "0007_resource_category"),
        ("lecturers", "0002_lecturerofsubject_subject_group"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="LecturerOfSubject",
            new_name="LecturerOfSubjectOfAgeGroup",
        ),
    ]
