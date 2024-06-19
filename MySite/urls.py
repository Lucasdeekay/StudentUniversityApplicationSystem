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
    path('reset-password/<int:user_id>', views.password_reset_view, name='password_reset'),
    path('logout/', views.logout_view, name='logout'),
    path('payment/', views.payment, name='payment'),
    path('verify/<str:reference>/', views.verify_payment, name='verify_payment'),
    path('api/', include(router.urls)),
]
