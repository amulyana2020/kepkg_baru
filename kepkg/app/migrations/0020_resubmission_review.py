# Generated by Django 4.2.16 on 2024-11-05 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_resubmission_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='resubmission',
            name='review',
            field=models.TextField(null=True, verbose_name='Hasil Review'),
        ),
    ]
