# Generated by Django 4.2.16 on 2024-11-02 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_profile_address_alter_profile_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='category',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='exemption_letter',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='status',
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENGAJUAN SUDAH DITERIMA', 'Pengajuan Sudah Diterima'), ('PENGAJUAN SEDANG DIPROSES', 'Pengajuan sedang diproses'), ('PENGAJUAN SELESAI', 'Pengajuan Selesai')], max_length=255)),
                ('category', models.CharField(blank=True, choices=[('EXEMPTED', 'Exempted'), ('EXPEDITED', 'Expedited'), ('FULLBOARD', 'Fullboard'), ('BELUM DITENTUKAN', 'Belum Ditentukan')], default='BELUM DITENTUKAN', max_length=120, null=True, verbose_name='Kategori Telaah')),
                ('exemption_letter', models.FileField(blank=True, null=True, upload_to='file/exemption_letter', verbose_name='Surat Pembebasan Telaah Etik')),
                ('submission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.submission')),
            ],
        ),
    ]
