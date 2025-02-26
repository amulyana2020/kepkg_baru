# Generated by Django 4.2.16 on 2024-11-02 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_submission_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['-submission']},
        ),
        migrations.AlterField(
            model_name='status',
            name='submission',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='submission', to='app.submission'),
        ),
    ]
