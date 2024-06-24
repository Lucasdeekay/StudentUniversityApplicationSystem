from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    JAMBAdmissionLetter, SchoolAcceptanceForm, JAMBResultSlip, OLevelResult,
    MedicalExaminationForm, ParentLetterOfUndertaking, GuarantorLetterOfUndertaking,
    BirthCertificate, LocalGovernmentCertification, StudentBioData, StudentRegistration, AcceptanceFeePayment
)
from .serializers import (
    JAMBAdmissionLetterSerializer, SchoolAcceptanceFormSerializer, JAMBResultSlipSerializer,
    OLevelResultSerializer, MedicalExaminationFormSerializer, ParentLetterOfUndertakingSerializer,
    GuarantorLetterOfUndertakingSerializer, BirthCertificateSerializer,
    LocalGovernmentCertificationSerializer, StudentBioDataSerializer, StudentRegistrationSerializer,
    AcceptanceFeePaymentSerializer
)


class JAMBAdmissionLetterViewSet(viewsets.ModelViewSet):
    queryset = JAMBAdmissionLetter.objects.all()
    serializer_class = JAMBAdmissionLetterSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed


class SchoolAcceptanceFormViewSet(viewsets.ModelViewSet):
    queryset = SchoolAcceptanceForm.objects.all()
    serializer_class = SchoolAcceptanceFormSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed


class JAMBResultSlipViewSet(viewsets.ModelViewSet):
    queryset = JAMBResultSlip.objects.all()
    serializer_class = JAMBResultSlipSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed


class OLevelResultViewSet(viewsets.ModelViewSet):
    queryset = OLevelResult.objects.all()
    serializer_class = OLevelResultSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed


class MedicalExaminationFormViewSet(viewsets.ModelViewSet):
    queryset = MedicalExaminationForm.objects.all()
    serializer_class = MedicalExaminationFormSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed


class ParentLetterOfUndertakingViewSet(viewsets.ModelViewSet):
    queryset = ParentLetterOfUndertaking.objects.all()
    serializer_class = ParentLetterOfUndertakingSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed


class GuarantorLetterOfUndertakingViewSet(viewsets.ModelViewSet):
    queryset = GuarantorLetterOfUndertaking.objects.all()
    serializer_class = GuarantorLetterOfUndertakingSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed


class BirthCertificateViewSet(viewsets.ModelViewSet):
    queryset = BirthCertificate.objects.all()
    serializer_class = BirthCertificateSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed


class LocalGovernmentCertificationViewSet(viewsets.ModelViewSet):
    queryset = LocalGovernmentCertification.objects.all()
    serializer_class = LocalGovernmentCertificationSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed


class AcceptanceFeePaymentViewSet(viewsets.ModelViewSet):
    queryset = AcceptanceFeePayment.objects.all()
    serializer_class = AcceptanceFeePaymentSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed


class StudentBioDataViewSet(viewsets.ModelViewSet):
    queryset = StudentBioData.objects.all()
    serializer_class = StudentBioDataSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed


class StudentRegistrationViewSet(viewsets.ModelViewSet):
    queryset = StudentRegistration.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed
