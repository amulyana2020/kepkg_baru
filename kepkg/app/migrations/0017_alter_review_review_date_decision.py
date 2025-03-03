# Generated by Django 4.2.16 on 2024-11-04 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_reviewer_reviewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_date',
            field=models.DateField(verbose_name='Tanggal Selesai Review'),
        ),
        migrations.CreateModel(
            name='Decision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_decision', models.FileField(upload_to='file/file_decision/', verbose_name='Unggah Laporan Telaah Akhir')),
                ('decision', models.CharField(blank=True, choices=[('DISETUJUI', 'Disetujui'), ('PERBAIKAN MINOR', 'Perbaikan Minor'), ('PERBAIKAN MAYOR', 'Perbaikan Mayor'), ('FULLBOARD', 'FullBoard')], max_length=255, null=True, verbose_name='Keputusan Akhir')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='decision', related_query_name='decision', to='app.submission')),
            ],
        ),
    ]
