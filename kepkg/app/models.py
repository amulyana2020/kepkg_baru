from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils.text import slugify

User.__str__ = lambda user_instance: f"{user_instance.first_name} {user_instance.last_name}"
# Create your models here.


GENDER_CHOICES = (
    ('LAKI-LAKI', _('Laki-laki')),
    ('PEREMPUAN', _('Perempuan')),
)

DECISION_CHOICES = (
    ("DISETUJUI", _('Disetujui')),
    ("PERBAIKAN MINOR", _('Perbaikan Minor')),
    ("PERBAIKAN MAYOR", _('Perbaikan Mayor')),
    ("FULLBOARD", _('FullBoard')),
)

DATA_CHOICES = (
    ('PRIMER', _('Primer')),
    ('SEKUNDER', _('Sekunder')),
)

STATUS_CHOICES = (
    ('PENGAJUAN SUDAH DITERIMA', _('Pengajuan Sudah Diterima')),
    ('PENGAJUAN SEDANG DIPROSES', _('Pengajuan sedang diproses')),
    ('PENGAJUAN SELESAI', _('Pengajuan Selesai')),
)

CATEGORY_CHOICES = (
    ('EXEMPTED', _('Exempted')),
    ('EXPEDITED', _('Expedited')),
    ('FULLBOARD', _('Fullboard')),
    ('BELUM DITENTUKAN', _('Belum Ditentukan')),
)

PRODI_CHOICES = (
    ('SARJANA', _('Sarjana')),
    ('PROFESI', _('Profesi')),
    ('MASTER', _('Master')),
    ('SPESIALIS', _('Spesialis')),
    ('DOKTOR', _('Doktor')),
    ('UMUM', _('Umum')),
    ('DOSEN', _('Dosen')),
)

SAMPLE_CHOICES = (
    ('PASIEN ATAU MASYARAKAT', _('Pasien atau Masyarakat')),
    ('BAHAN BIOLOGIS TERSIMPAN', _('Bahan Biologis Tersimpan')),
    ('REKAM MEDIK', _('Rekam Medik (Termasuk Foto Radiografik, Model Gigi)')),
    ('MATERIAL NON BIOLOGIS', _('Material Non Biologis')),
)

class News(models.Model):
    title = models.CharField(verbose_name="Judul Berita", max_length=255, null=False, blank=False)
    content = RichTextField(null=True, blank=True, verbose_name="Isi Berita", default="Tidak ada berita")
    created_at = models.DateField(auto_now_add=True)
    slug = AutoSlugField(populate_from='title', max_length=150, default="")

    def __str__(self):
        return '%s %s' % (self.title, self.created_at)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])

    def get_update_url(self):
        return reverse('news_update', args=[self.slug])

    def get_delete_url(self):
        return reverse('news_delete', args=[self.slug])

    def get_news_list(self):
        return reverse('news_list')

class Profile(models.Model):
  fullname = models.CharField(verbose_name="Nama lengkap beserta gelar", max_length=250, null=True, blank=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  photo = models.ImageField(verbose_name="Foto", upload_to='images/photo', null=True, blank=True)
  dob = models.DateField(verbose_name="Tanggal Lahir", null=True, blank=True)
  gender = models.CharField(_('Jenis Kelamin'),
                                         choices=GENDER_CHOICES,
                                         blank=True,
                                         null=True, max_length=255)
  address = models.CharField(verbose_name="Alamat", max_length=250, null=True, blank=True)
  city =  models.CharField(verbose_name="Kota", max_length=250, null=True, blank=True)
  phone = models.CharField(verbose_name="Telepon", max_length=15, null=True, blank=True)
  mobile = models.CharField(verbose_name="Nomor Handphone", max_length=15,null=True, blank=True )

  def __str__(self):
      return '%s %s' % (self.user.first_name, self.user.last_name)


  class Meta:
      ordering=["user__first_name"]


class Submission(models.Model):
    user = models.ForeignKey(User, related_name='author', verbose_name="Nama Peneliti", on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="Judul Penelitian", null=False, blank=False)
    study_program = models.CharField(max_length=500, choices=PRODI_CHOICES, verbose_name="Program Studi", null=False, blank=False)
    sample_or_subject = models.CharField(max_length=500, choices=SAMPLE_CHOICES, verbose_name="Sample / Subject", null=False, blank=False)
    data = models.CharField(max_length=255, choices=DATA_CHOICES, verbose_name="Data Primer/Sekunder", default="PRIMER", null=False, blank=False)
    submission_file = models.FileField(upload_to='file/submission/', verbose_name="Formulir Pengajuan (Dokumen A)", null=False, blank=False)
    consent_file = models.FileField(upload_to='file/consent/', verbose_name="Informed Consent", null=True, blank=True)
    agreement_file = models.FileField(upload_to='file/agreement/', verbose_name="Lembar Persetujuan", null=False, blank=False)
    institution_letter = models.FileField(upload_to='file/institution_letter/', verbose_name="Surat Pengantar dari Institusi", null=False, blank=False)
    statement_letter = models.FileField(upload_to='file/statement_letter/', verbose_name="Surat Pernyataan penelitian belum dilaksanakan sebelum pengajuan kelaikan etik", null=False, blank=False)
    peer_group_form = models.FileField(upload_to='file/peer_group_form/', verbose_name="Kajian ilmiah oleh peer group atau departemen terkait", null=False, blank=False)
    curriculum_vitae = models.FileField(upload_to='file/curriculum_vitae/', verbose_name="Biodata peneliti tentang penelitian yang telah dilaksanakan", null=False, blank=False)
    payment = models.FileField(upload_to='file/payment/', null=False, blank=False,
                                        verbose_name="Bukti Pembayaran")
    created_at = models.DateField(auto_now_add=True)
    slug = AutoSlugField(populate_from='title', max_length=150)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return '%s %s - %s' % (self.user.first_name, self.user.last_name, self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Submission, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('submission_detail', args=[self.slug])

    def get_update_url(self):
        return reverse('submission_update', args=[self.slug])

    def get_delete_url(self):
        return reverse('submission_delete', args=[self.slug])

    def get_my_submission(self):
        return reverse('my_submission_list')

    def get_submission(self):
        return reverse('submission_list')


class Status(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name="status")
    status = models.CharField(max_length=255, null=False, blank=False, choices=STATUS_CHOICES)
    category = models.CharField(max_length=120, choices=CATEGORY_CHOICES, verbose_name="Kategori Telaah", null=True, blank=True, default='BELUM DITENTUKAN')
    exemption_letter = models.FileField(upload_to="file/exemption_letter", verbose_name="Surat Pembebasan Telaah Etik", null=True, blank=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-submission"]

    def __str__(self):
        return '%s - %s' % (self.submission, self.status)


class Review(models.Model):
    description = RichTextField(verbose_name="Hasil Review", null=True, blank=True, default='')
    file_review = models.FileField(upload_to='file/file_review/', null=True, blank=True,
                                        verbose_name="Upload hasil review (Dokumen D) ")
    decision = models.CharField(max_length=255, verbose_name="Keputusan", choices=DECISION_CHOICES)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='reviews',
                                related_query_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', related_query_name='review')
    review_date = models.DateField(verbose_name="Tanggal Selesai Review")
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return '%s %s  -- %s --%s' % (self.reviewer.first_name, self.reviewer.last_name, self.reviewer.email, self.decision)


class Reviewer(models.Model):
    submission = models.ForeignKey(Submission,on_delete=models.CASCADE, related_name="reviewer")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewers', related_query_name='reviewer', null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return '%s' % (self.reviewer)

    def get_absolute_url(self):
        return reverse('reviewer_detail', args=[self.pk])

    def get_update_url(self):
        return reverse('reviewer_update', args=[self.pk])

    def get_delete_url(self):
        return reverse('reviewer_delete', args=[self.pk])

    def get_submission_url(self):
        return reverse('submission_detail', args=[self.submission.slug])


class Decision(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='decision',
                                   related_query_name='decision')
    file_decision = models.FileField(upload_to="file/file_decision/", null=False, blank=False,
                                        verbose_name="Unggah Laporan Telaah Akhir")
    decision = models.CharField(max_length=255, verbose_name="Keputusan Akhir", choices=DECISION_CHOICES, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return ' %s' % (self.submission.title)


class Resubmission(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='submission',
                                   related_query_name='submission')
    resubmission_document = models.FileField(upload_to="file/resubmission_document/", null=False, blank=False,
                                     verbose_name="Unggah Dokumen Revisi (Dokumen F)")
    review = models.TextField(verbose_name="Hasil Review", null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return ' %s' % (self.submission.title)


    def get_absolute_url(self):
        return reverse('resubmission_detail', args=[self.pk])



class ReviewResubmission(models.Model):
    description = RichTextField(verbose_name="Hasil Review Resubmission", null=True, blank=True, default='')
    file_review = models.FileField(upload_to='file/file_review/', null=True, blank=True,
                                        verbose_name="Upload hasil review (Dokumen D) ")
    decision = models.CharField(max_length=255, verbose_name="Keputusan", choices=DECISION_CHOICES)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='reviews_resubmission',
                                related_query_name='review_resubmission', null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_resubmission', related_query_name='review_resubmission')
    review_date = models.DateField(verbose_name="Tanggal Selesai Review")
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return '%s %s  -- %s --%s' % (self.reviewer.first_name, self.reviewer.last_name, self.reviewer.email, self.decision)



class Amandement(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='amandement',
                                   related_query_name='amandement')
    amandement_document = models.FileField(upload_to="file/amandement_document/", null=False, blank=False,
                                     verbose_name="Unggah Dokumen Revisi (Dokumen G)")
    review = models.TextField(verbose_name="Hasil Review", null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return ' %s' % (self.submission.title)


    def get_absolute_url(self):
        return reverse('amandement_detail', args=[self.pk])
