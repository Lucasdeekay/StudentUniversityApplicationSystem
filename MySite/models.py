from django.db import models
from django.contrib.auth.models import User


class JAMBAdmissionLetter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='jamb_admission_letters/')


class SchoolAcceptanceForm(models.Model):
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
    file = models.FileField(upload_to='letters_of_undertaking/')


class GuarantorLetterOfUndertaking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=50, choices=[
        ('CLERGY', 'Clergy'),
        ('CLERIC', 'Cleric'),  # Corrected typo (optional)
        ('PUBLIC_SERVANT', 'Public Servant'),
    ])
    file = models.FileField(upload_to='letters_of_undertaking/')


class BirthCertificate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='birth_certificates/')


class LocalGovernmentCertification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='local_gov_certifications/')


class AcceptanceFeePayment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fee = models.IntegerField(default=30000)
    status = models.BooleanField(default=False)


class StudentBioData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='student_bio_data/')


class StudentRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acceptance_fee = models.ForeignKey(AcceptanceFeePayment, on_delete=models.CASCADE, null=True, blank=True)
    jamb_admission_letter = models.ForeignKey(JAMBAdmissionLetter, on_delete=models.CASCADE, null=True, blank=True)
    school_acceptance_form = models.ForeignKey(SchoolAcceptanceForm, on_delete=models.CASCADE, null=True, blank=True)
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
    registration_status = models.CharField(max_length=100, choices=[
        ('Pending Payment', 'Pending Payment'),
        ('Upload All Documents', 'Upload All Documents'),
        ('Re-upload JAMB Admission Letter', 'Re-upload JAMB Admission Letter'),
        ('Re-upload School Acceptance Form', 'Re-upload School Acceptance Form'),
        ('Re-upload JAMB Result Slip', 'Re-upload JAMB Result Slip'),
        ('Re-upload O\'Level Result', 'Re-upload O\'Level Result'),
        ('Re-upload Medical Examination Form', 'Re-upload Medical Examination Form'),
        ('Re-upload Parent Letter Of Undertaking', 'Re-upload Parent Letter Of Undertaking'),
        ('Re-upload Guarantor Letter Of Undertaking', 'Re-upload Guarantor Letter Of Undertaking'),
        ('Re-upload Birth Certificate', 'Re-upload Birth Certificate'),
        ('Re-upload Local Government Certification', 'Re-upload Local Government Certification'),
        ('Re-upload Bio-data', 'Re-upload Bio-data'),
        ('Re-upload All Documents', 'Re-upload All Documents'),
        ('Completed', 'Completed'),
    ], default='Pending Payment')

    def __str__(self):
        return f"{self.user.username} - {self.registration_status}"


