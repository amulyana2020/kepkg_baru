# Generated by Django 4.2.16 on 2025-02-23 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_submission_sample_or_subject_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='consent_file',
            field=models.FileField(blank=True, null=True, upload_to='file/consent/', verbose_name='Informed Consent'),
        ),
    ]
