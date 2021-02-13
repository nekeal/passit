# Generated by Django 2.2.6 on 2020-05-01 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20200501_1933'),
        ('subject', '0010_subject_syllabus_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='image',
        ),
        migrations.CreateModel(
            name='ResourceAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='resource_attachments', to='files.File')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subject.Resource')),
            ],
        ),
        migrations.AddField(
            model_name='resource',
            name='files',
            field=models.ManyToManyField(blank=True, through='subject.ResourceAttachment', to='files.File'),
        ),
    ]
