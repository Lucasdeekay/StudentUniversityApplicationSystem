from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .viewsets import JAMBAdmissionLetterViewSet, SchoolAdmissionLetterViewSet, JAMBResultSlipViewSet, \
    OLevelResultViewSet, MedicalExaminationFormViewSet, ParentLetterOfUndertakingViewSet, \
    GuarantorLetterOfUndertakingViewSet, BirthCertificateViewSet, LocalGovernmentCertificationViewSet, \
    StudentBioDataViewSet, StudentRegistrationViewSet, AcceptanceFeePaymentViewSet

router = DefaultRouter()
router.register(r'admission-letters', JAMBAdmissionLetterViewSet)
router.register(r'school-admission-letters', SchoolAdmissionLetterViewSet)
router.register(r'jamb-result-slips', JAMBResultSlipViewSet)
router.register(r'o-level-results', OLevelResultViewSet)
router.register(r'medical-examination-forms', MedicalExaminationFormViewSet)
router.register(r'parent-letters-of-undertaking', ParentLetterOfUndertakingViewSet)
router.register(r'guarantor-letters-of-undertaking', GuarantorLetterOfUndertakingViewSet)
router.register(r'birth-certificates', BirthCertificateViewSet)
router.register(r'local-government-certifications', LocalGovernmentCertificationViewSet)
router.register(r'acceptance-fee-payments', AcceptanceFeePaymentViewSet)
router.register(r'student-bio-data', StudentBioDataViewSet)
router.register(r'student-registrations', StudentRegistrationViewSet)

urlpatterns = [
    path('', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('reset-password/', views.password_reset_view, name='password_reset'),
    path('logout/', views.logout_view, name='logout'),
    path('payment/', views.payment, name='payment'),
    path('dashboard/', views.user_profile, name='user_dashboard'),
    path('verify/<str:reference>/', views.verify_payment, name='verify_payment'),
    path('process-registration/', views.student_registration, name='student_registration'),
    path('update-registration/', views.student_registration_update, name='student_registration_update'),
    path('download-acceptance-fee-slip/', views.download_acceptance_fee_slip, name='download_acceptance_fee_slip'),
    path('download-registration-clearance-fee-slip/', views.download_registration_clearance_fee_slip, name='download_registration_clearance_fee_slip'),
    path('api/', include(router.urls)),
]
