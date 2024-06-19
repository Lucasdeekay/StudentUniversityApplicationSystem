from django.db import models
from django.contrib.auth.models import User


class JAMBAdmissionLetter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='jamb_admission_letters/')


class SchoolAdmissionLetter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='school_admission_letters/')


class JAMBResultSlip(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='jamb_results/')


class OLevelResult(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[
        ('WAEC', 'WAEC'),
        ('NECO', 'NECO'),
    ])
    file = models.FileField(upload_to='o_level_results/')


class MedicalExaminationForm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='medical_forms/')


class ParentLetterOfUndertaking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=50, choices=[
        ('PARENT', 'Parent'),
        ('GUARDIAN', 'Guardian'),
    ])
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='letters_of_undertaking/')


class GuarantorLetterOfUndertaking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=50, choices=[
        ('CLERGY', 'Clergy'),
        ('CLERIC', 'Cleric'),  # Corrected typo (optional)
        ('PUBLIC_SERVANT', 'Public Servant'),
    ])
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='letters_of_undertaking/')


class BirthCertificate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='birth_certificates/')


class LocalGovernmentCertification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='local_gov_certifications/')


class AcceptanceFeePayment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=6, decimal_places=2, default=30000)
    status = models.BooleanField(default=False)


class StudentBioData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='student_bio_data/')


class StudentRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acceptance_fee = models.ForeignKey(AcceptanceFeePayment, on_delete=models.CASCADE)
    jamb_admission_letter = models.ForeignKey(JAMBAdmissionLetter, on_delete=models.CASCADE)
    school_admission_letter = models.ForeignKey(SchoolAdmissionLetter, on_delete=models.CASCADE, null=True, blank=True)
    jamb_result_slip = models.ForeignKey(JAMBResultSlip, on_delete=models.CASCADE, null=True, blank=True)
    o_level_result = models.ForeignKey(OLevelResult, on_delete=models.CASCADE, null=True, blank=True)
    medical_examination_form = models.ForeignKey(MedicalExaminationForm, on_delete=models.CASCADE, null=True,
                                                 blank=True)
    letter_of_undertaking_parent = models.ForeignKey(ParentLetterOfUndertaking, on_delete=models.CASCADE, null=True,
                                                     blank=True, related_name='parent_undertaking')
    letter_of_undertaking_guarantor = models.ForeignKey(GuarantorLetterOfUndertaking, on_delete=models.CASCADE,
                                                        null=True, blank=True, related_name='guarantor_undertaking')
    birth_certificate = models.ForeignKey(BirthCertificate, on_delete=models.CASCADE, null=True, blank=True)
    local_government_certification = models.ForeignKey(LocalGovernmentCertification, on_delete=models.CASCADE,
                                                       null=True, blank=True)
    bio_data = models.ForeignKey(StudentBioData, on_delete=models.CASCADE, null=True, blank=True)
    registration_status = models.CharField(max_length=20, choices=[
        ('PENDING_PAYMENT', 'Pending Payment'),
        ('DOCUMENTS_PENDING', 'Documents Pending'),
        ('BIO_PENDING', 'Bio-data Pending'),
        ('COMPLETED', 'Completed'),
    ], default='PENDING_PAYMENT')

    def __str__(self):
        return f"{self.user.username} - {self.registration_status}"


