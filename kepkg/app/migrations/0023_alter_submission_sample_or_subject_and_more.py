# Generated by Django 4.2.16 on 2025-02-23 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_amandement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='sample_or_subject',
            field=models.CharField(choices=[('PASIEN ATAU MASYARAKAT', 'Pasien atau Masyarakat'), ('BAHAN BIOLOGIS TERSIMPAN', 'Bahan Biologis Tersimpan'), ('REKAM MEDIK', 'Rekam Medik (Termasuk Foto Radiografik, Model Gigi)'), ('MATERIAL NON BIOLOGIS', 'Material Non Biologis')], max_length=500, verbose_name='Sample / Subject'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='study_program',
            field=models.CharField(choices=[('SARJANA', 'Sarjana'), ('PROFESI', 'Profesi'), ('MASTER', 'Master'), ('SPESIALIS', 'Spesialis'), ('DOKTOR', 'Doktor'), ('UMUM', 'Umum'), ('DOSEN', 'Dosen')], max_length=500, verbose_name='Program Studi'),
        ),
    ]
