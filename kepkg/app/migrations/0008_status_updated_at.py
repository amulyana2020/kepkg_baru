# Generated by Django 4.2.16 on 2024-11-02 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_status_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
