# Generated by Django 2.2.6 on 2020-02-10 15:18

from django.db import migrations, models
import django.db.models.deletion
import subject.models

from subject.models import FieldOfStudyOfAgeGroup, FieldOfStudy


def default_field_group():
    default_field_of_study, _ = FieldOfStudy.objects.get_or_create(name='default field', slug='default-field')
    default_field_age_group, _ = FieldOfStudyOfAgeGroup.objects.get_or_create(field_of_study=default_field_of_study,
                                                                              students_start_year=2000)
    return default_field_age_group.id


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0003_auto_20200207_2021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjectofagegroup',
            name='students_start_year',
        ),
        migrations.CreateModel(
            name='FieldOfStudyOfAgeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('students_start_year', models.PositiveIntegerField(validators=[subject.models.year_validator])),
                ('field_of_study', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='age_groups', to='subject.FieldOfStudy')),
            ],
        ),
        migrations.AddField(
            model_name='subjectofagegroup',
            name='field_age_group',
            field=models.ForeignKey(default=default_field_group, on_delete=django.db.models.deletion.PROTECT, related_name='subject_groups', to='subject.FieldOfStudyOfAgeGroup'),
            preserve_default=False,
        ),
    ]
