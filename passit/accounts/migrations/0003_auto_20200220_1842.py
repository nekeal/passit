# Generated by Django 2.2.6 on 2020-02-20 18:42
import django.db.models.deletion
from django.db import migrations, models

import passit


class Migration(migrations.Migration):

    dependencies = [
        ("subject", "0004_auto_20200210_1518"),
        ("accounts", "0002_userprofile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Membership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "REPRESENTATIVE"),
                            (2, "MODERATOR"),
                            (3, "NORMAL"),
                        ],
                        default=passit.accounts.models.MembershipTypeChoices(3),
                    ),
                ),
                (
                    "field_age_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberships",
                        to="subject.FieldOfStudyOfAgeGroup",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberships",
                        to="accounts.UserProfile",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="userprofile",
            name="field_age_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="students",
                through="accounts.Membership",
                to="subject.FieldOfStudyOfAgeGroup",
            ),
        ),
    ]
