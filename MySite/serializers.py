from rest_framework import serializers
from .models import (
    JAMBAdmissionLetter, SchoolAdmissionLetter, JAMBResultSlip, OLevelResult,
    MedicalExaminationForm, ParentLetterOfUndertaking, GuarantorLetterOfUndertaking,
    BirthCertificate, LocalGovernmentCertification, StudentBioData, StudentRegistration, AcceptanceFeePayment
)
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Add additional user fields as needed


class JAMBAdmissionLetterSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = JAMBAdmissionLetter
        fields = '__all__'


class SchoolAdmissionLetterSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = SchoolAdmissionLetter
        fields = '__all__'


class JAMBResultSlipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = JAMBResultSlip
        fields = '__all__'


class OLevelResultSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = OLevelResult
        fields = '__all__'


class MedicalExaminationFormSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MedicalExaminationForm
        fields = '__all__'


class ParentLetterOfUndertakingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ParentLetterOfUndertaking
        fields = '__all__'


class GuarantorLetterOfUndertakingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GuarantorLetterOfUndertaking
        fields = '__all__'


class BirthCertificateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BirthCertificate
        fields = '__all__'


class LocalGovernmentCertificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = LocalGovernmentCertification
        fields = '__all__'


class AcceptanceFeePaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AcceptanceFeePayment
        fields = '__all__'


class StudentBioDataSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentBioData
        fields = '__all__'  # Add additional bio-data fields as needed


class StudentRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    jamb_admission_letter = JAMBAdmissionLetterSerializer(read_only=True)
    school_admission_letter = SchoolAdmissionLetterSerializer(read_only=True)
    jamb_result_slip = JAMBResultSlipSerializer(read_only=True)
    o_level_result = OLevelResultSerializer(read_only=True)
    medical_examination_form = MedicalExaminationFormSerializer(read_only=True)
    letter_of_undertaking_parent = ParentLetterOfUndertakingSerializer(read_only=True)
    letter_of_undertaking_guarantor = GuarantorLetterOfUndertakingSerializer(read_only=True)
    birth_certificate = BirthCertificateSerializer(read_only=True)
    local_government_certification = LocalGovernmentCertificationSerializer(read_only=True)
    bio_data = StudentBioDataSerializer(read_only=True)

    class Meta:
        model = StudentRegistration
        fields = '__all__'  # Include all fields in the serializer
