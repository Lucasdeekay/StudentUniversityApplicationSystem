from django.contrib import admin
from .models import (
    JAMBAdmissionLetter, SchoolAcceptanceForm, JAMBResultSlip, OLevelResult,
    MedicalExaminationForm, ParentLetterOfUndertaking, GuarantorLetterOfUndertaking,
    BirthCertificate, LocalGovernmentCertification, StudentBioData, StudentRegistration, AcceptanceFeePayment
)


@admin.register(JAMBAdmissionLetter)
class JAMBAdmissionLetterAdmin(admin.ModelAdmin):
    list_display = ('user', 'file')


@admin.register(SchoolAcceptanceForm)
class SchoolAcceptanceFormAdmin(admin.ModelAdmin):
    list_display = ('user', 'file')


@admin.register(JAMBResultSlip)
class JAMBResultSlipAdmin(admin.ModelAdmin):
    list_display = ('user', 'file')


@admin.register(OLevelResult)
class OLevelResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'file')


@admin.register(MedicalExaminationForm)
class MedicalExaminationFormAdmin(admin.ModelAdmin):
    list_display = ('user', 'file')


@admin.register(ParentLetterOfUndertaking)
class ParentLetterOfUndertakingAdmin(admin.ModelAdmin):
    list_display = ('user', 'relationship', 'file')


@admin.register(GuarantorLetterOfUndertaking)
class GuarantorLetterOfUndertakingAdmin(admin.ModelAdmin):
    list_display = ('user', 'relationship', 'file')


@admin.register(BirthCertificate)
class BirthCertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'file')


@admin.register(LocalGovernmentCertification)
class LocalGovernmentCertificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'file')


@admin.register(AcceptanceFeePayment)
class AcceptanceFeePaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'fee', 'status')


@admin.register(StudentBioData)
class StudentBioDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'file')


@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio_data', 'registration_status')
