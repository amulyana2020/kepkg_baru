# Generated by Django 4.2.16 on 2024-11-03 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_reviewer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewer',
            name='user',
        ),
        migrations.AddField(
            model_name='reviewer',
            name='reviewer',
            field=models.ManyToManyField(related_name='reviewers', related_query_name='reviewer', to='app.profile'),
        ),
    ]
