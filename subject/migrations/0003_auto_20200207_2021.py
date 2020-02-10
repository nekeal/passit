# Generated by Django 2.2.6 on 2020-02-07 20:21
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0002_fieldofstudies_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='field_of_studies',
            new_name='field_of_study',
        ),
        migrations.RenameModel(
            old_name='FieldOfStudies',
            new_name='FieldOfStudy',
        ),
        migrations.AlterField(
            model_name='subject',
            name='field_of_study',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subjects',
                                    to='subject.FieldOfStudy'),
        ),
    ]
