import uuid
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from paystackapi import transaction
from reportlab.pdfgen import canvas

from .models import (
    JAMBAdmissionLetter, SchoolAdmissionLetter, JAMBResultSlip, OLevelResult,
    MedicalExaminationForm, ParentLetterOfUndertaking, GuarantorLetterOfUndertaking,
    BirthCertificate, LocalGovernmentCertification, StudentRegistration, AcceptanceFeePayment, StudentBioData
)


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to successful login page
            return redirect('user_dashboard')  # Replace 'home' with your desired redirect URL
        else:
            # Invalid login credentials
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'change_password.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email'].strip()
        try:
            user = User.objects.get(email=email)
            return redirect('password_reset', args=(user.id,))
        except User.DoesNotExist:
            messages.error(request, 'Email address not found.')
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')


def password_reset_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid user ID.')
        return redirect('password_reset')

    if request.method == 'POST':
        new_password1 = request.POST['new_password1'].strip()
        new_password2 = request.POST['new_password2'].strip()
        if new_password1 != new_password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('password_reset')
        # Set the new password
        user.set_password(new_password1)
        user.save()
        messages.success(request, 'Password reset successfully!')
        return redirect('password_reset')
    return render(request, 'password_reset.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user

        # Check if the old password is correct
        if not user.check_password(old_password):
            messages.error(request, 'Your old password was entered incorrectly. Please enter it again.')
            return redirect('change_password')

        # Check if the new passwords match
        if new_password1 != new_password2:
            messages.error(request, 'The two new password fields didn\'t match.')
            return redirect('change_password')

        # Update the user's password
        user.set_password(new_password1)
        user.save()

        # Update the user's session to reflect the password change
        update_session_auth_hash(request, user)

        messages.success(request, 'Your password was successfully updated!')
        return redirect('change_password')

    return render(request, 'change_password.html')


def verify_payment(request, reference):
    response = transaction.Transaction.verify(reference)

    if response['status'] and response['data']['status'] == 'success':
        acceptance = AcceptanceFeePayment(user=request.user)
        acceptance.status = True
        acceptance.save()
        messages.success(request, f"Acceptance fee successfully paid.")
        return redirect('user_dashboard')
    else:
        messages.error(request, 'Payment verification failed')
        return redirect('user_dashboard')


@login_required
def payment(request):
    fee = get_object_or_404(AcceptanceFeePayment, user=request.user)

    # Initialize transaction
    response = transaction.Transaction.initialize(
        reference=str(uuid.uuid4()),
        amount=float(fee.fee) * 100,
        email=request.user.email
    )

    if response['status']:
        return HttpResponseRedirect(response['data']['authorization_url'])

    return render(request, 'deposit.html')

@login_required
def student_registration(request):
    if request.method == 'POST':
        # Check if user has paid acceptance fee
        user = request.user
        payment_made = AcceptanceFeePayment.objects.get(user=user)
        if not payment_made.status:
            return redirect('payment')  # Replace 'payment_page' with your actual payment page URL

        # Process registration details (excluding bio-data)
        jamb_letter = request.FILES.get('jamb_admission_letter')
        school_letter = request.FILES.get('school_admission_letter')
        jamb_slip = request.FILES.get('jamb_result_slip')
        o_level_result = request.FILES.get('o_level_result')
        o_level_type = request.FILES.get('o_level_type').strip()
        medical_form = request.FILES.get('medical_examination_form')
        parent_letter = request.FILES.get('parent_letter_of_undertaking')
        parent_name = request.POST.get('parent_name').strip()
        parent_relationship = request.POST.get('parent_relationship').strip()
        guarantor_letter = request.FILES.get('guarantor_letter_of_undertaking')
        guarantor_name = request.POST.get('guarantor_name').strip()
        guarantor_relationship = request.POST.get('guarantor_relationship').strip()
        birth_certificate = request.FILES.get('birth_certificate')
        local_government_cert = request.FILES.get('local_government_certification')
        bio_data = request.FILES.get('bio_data')

        # Check if all required documents are uploaded
        if not all([jamb_letter, school_letter, jamb_slip, o_level_result, medical_form, parent_letter, guarantor_letter, birth_certificate, local_government_cert, bio_data]):
            message = 'Please upload all required documents.'
            return render(request, 'registration_form.html', {'message': message})

        # Save registration details (excluding bio-data)
        registration, created = StudentRegistration.objects.get_or_create(user=user)
        if created:
            registration.acceptance_fee = AcceptanceFeePayment.objects.get(user=user)
        registration.jamb_admission_letter = JAMBAdmissionLetter.objects.create(user=user, file=jamb_letter)
        registration.school_admission_letter = SchoolAdmissionLetter.objects.create(user=user, file=school_letter)
        registration.jamb_result_slip = JAMBResultSlip.objects.create(user=user, file=jamb_slip)
        registration.o_level_result = OLevelResult.objects.create(user=user, type=o_level_type, file=o_level_result)
        registration.medical_examination_form = MedicalExaminationForm.objects.create(user=user, file=medical_form)
        registration.letter_of_undertaking_parent = ParentLetterOfUndertaking.objects.create(user=user, name=parent_name, relationship=parent_relationship, file=parent_letter)
        registration.letter_of_undertaking_guarantor = GuarantorLetterOfUndertaking.objects.create(user=user, name=guarantor_name, relationship=guarantor_relationship, file=guarantor_letter)
        registration.birth_certificate = BirthCertificate.objects.create(user=user, file=birth_certificate)
        registration.local_government_certification = LocalGovernmentCertification.objects.create(user=user, file=local_government_cert)
        registration.bio_data = StudentBioData.objects.create(user=user, file=bio_data)
        registration.save()

        message = 'Registration successful!'
        return render(request, 'registration_form.html', {'message': message})

    else:
        # Display registration form
        return render(request, 'registration_form.html')


@login_required
def student_registration_update(request):
    if request.method == 'POST':
        # Check if user has paid acceptance fee
        user = request.user
        payment_made = AcceptanceFeePayment.objects.filter(user=user, status=True).exists()
        if not payment_made:
            return redirect('payment_page')  # Replace 'payment_page' with your actual payment page URL

        # Get existing registration object
        registration = StudentRegistration.objects.get(user=user)

        # Process registration details (excluding bio-data)
        update_data = {}  # Dictionary to store data for update

        # Update JAMB Admission Letter
        if request.FILES.get('jamb_admission_letter'):
            jamb_letter_instance, created = JAMBAdmissionLetter.objects.get_or_create(user=user)
            jamb_letter_instance.file = request.FILES.get('jamb_admission_letter')
            jamb_letter_instance.save()
            update_data['jamb_admission_letter'] = jamb_letter_instance

        # Update School Admission Letter
        if request.FILES.get('school_admission_letter'):
            school_letter_instance, created = SchoolAdmissionLetter.objects.get_or_create(user=user)
            school_letter_instance.file = request.FILES.get('school_admission_letter')
            school_letter_instance.save()
            update_data['school_admission_letter'] = school_letter_instance

        # Update JAMB Result Slip
        if request.FILES.get('jamb_result_slip'):
            jamb_slip_instance, created = JAMBResultSlip.objects.get_or_create(user=user)
            jamb_slip_instance.file = request.FILES.get('jamb_result_slip')
            jamb_slip_instance.save()
            update_data['jamb_result_slip'] = jamb_slip_instance

        # Update O'Level Result
        if request.FILES.get('o_level_result'):
            o_level_type = request.FILES.get('o_level_type').strip()
            if o_level_type:
                o_level_instance, created = OLevelResult.objects.get_or_create(user=user)
                o_level_instance.type = o_level_type
                o_level_instance.file = request.FILES.get('o_level_result')
                o_level_instance.save()
                update_data['o_level_result'] = o_level_instance
            else:
                message = 'O\'Level Result requires a type (WAEC or NECO).'
                return render(request, 'registration_form.html', {'message': message})

        # Update Medical Examination Form
        if request.FILES.get('medical_examination_form'):
            medical_form_instance, created = MedicalExaminationForm.objects.get_or_create(user=user)
            medical_form_instance.file = request.FILES.get('medical_examination_form')
            medical_form_instance.save()
            update_data['medical_examination_form'] = medical_form_instance

        # Update Parent Details
        parent_update = {}
        if request.FILES.get('parent_letter_of_undertaking'):
            parent_update['file'] = request.FILES.get('parent_letter_of_undertaking')
        if request.POST.get('parent_name'):
            parent_update['name'] = request.POST.get('parent_name').strip()
        if request.POST.get('parent_relationship'):
            parent_update['relationship'] = request.POST.get('parent_relationship').strip()

        if parent_update:
            registration.letter_of_undertaking_parent.update(**parent_update)

        # Update Guarantor Details
        guarantor_update = {}
        if request.FILES.get('guarantor_letter_of_undertaking'):
            guarantor_update['file'] = request.FILES.get('guarantor_letter_of_undertaking')
        if request.POST.get('guarantor_name'):
            guarantor_update['name'] = request.POST.get('guarantor_name').strip()
        if request.POST.get('guarantor_relationship'):
            guarantor_update['relationship'] = request.POST.get('guarantor_relationship').strip()

        if guarantor_update:
            registration.letter_of_undertaking_guarantor.update(**guarantor_update)

        # Update Birth Certificate
        if request.FILES.get('birth_certificate'):
            birth_certificate_instance, created = BirthCertificate.objects.get_or_create(user=user)
            birth_certificate_instance.file = request.FILES.get('birth_certificate')
            birth_certificate_instance.save()
            update_data['birth_certificate'] = birth_certificate_instance

        # Update Local Government Certification
        if request.FILES.get('local_government_certification'):
            local_government_cert_instance, created = LocalGovernmentCertification.objects.get_or_create(user=user)
            local_government_cert_instance.file = request.FILES.get('local_government_certification')
            local_government_cert_instance.save()
            update_data['local_government_certification'] = local_government_cert_instance

        # Update Student Bio Data
        if request.FILES.get('bio_data'):
            bio_data, created = StudentBioData.objects.get_or_create(user=user)
            bio_data.file = request.FILES.get('bio_data')
            bio_data.save()
            update_data['bio_data'] = bio_data

        # Update registration object with collected data
        if update_data:
            registration.update(**update_data)

            message = 'Registration details updated successfully!'
            return render(request, 'registration_form.html', {'message': message})

        else:
            # Display registration form
            return render(request, 'registration_form.html')

    else:
        # Display registration form
        return render(request, 'registration_form.html')


@login_required
def user_profile(request):
    user = request.user

    # Check registration status
    registration = StudentRegistration.objects.filter(user=user).first()

    context = {
        'user': user,
        'registration_status': registration.status,
    }

    return render(request, 'user_profile.html', context)


@login_required
def download_acceptance_fee_slip(request):
    user = request.user

    # Check if user has paid acceptance fee
    acceptance_fee = AcceptanceFeePayment.objects.filter(user=user, status=True).first()

    # Get user details and payment information
    amount_paid = acceptance_fee.amount
    payment_date = acceptance_fee.payment_date.strftime('%d %B, %Y')  # Format date

    # Set up PDF generation
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Acceptance_Fee_Slip.pdf"'
    buffer = canvas.Canvas(response)

    # Institution details (replace with your information)
    institution_name = "Dominion University"
    logo_path = "path/to/your/institution_logo.jpg"  # Replace with actual path

    # Add institution logo
    if logo_path:
        logo_width = 100
        logo_height = 50
        buffer.drawImage(logo_path, 20, 700, logo_width, logo_height)

    # Add institution name
    buffer.setFont("Helvetica-Bold", 24)
    buffer.drawString(200, 720, institution_name)

    # Add title
    buffer.setFont("Helvetica-Bold", 16)
    buffer.drawString(100, 680, "Acceptance Fee Slip")

    # Add user details
    buffer.setFont("Helvetica", 12)
    buffer.drawString(50, 650, f"Student Name: {user.first_name} {user.last_name}")

    # Add payment details
    buffer.drawString(50, 630, f"Amount Paid: ₦{amount_paid:.2f}")
    buffer.drawString(50, 610, f"Payment Date: {payment_date}")

    # Draw a separator line
    buffer.line(50, 600, 550, 600)

    # Add footer text
    buffer.setFont("Helvetica", 10)
    buffer.drawString(50, 580, f"This is a computer-generated document and does not require a signature.")

    buffer.save()
    return response


@login_required
def download_registration_clearance_fee_slip(request):
    user = request.user

    # Get user details and registration information
    registration = StudentRegistration.objects.get(user=user)
    full_name = f"{user.first_name} {user.last_name}"
    today = datetime.date.today().strftime('%d %B, %Y')  # Format date

    # Set up PDF generation
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Registration_Clearance_Fee_Slip.pdf"'
    buffer = canvas.Canvas(response)

    # Institution details (replace with your information)
    institution_name = "Dominion University"
    logo_path = "path/to/your/institution_logo.jpg"  # Replace with actual path

    # Add institution logo
    if logo_path:
        logo_width = 100
        logo_height = 50
        buffer.drawImage(logo_path, 20, 700, logo_width, logo_height)

    # Add institution name
    buffer.setFont("Helvetica-Bold", 24)
    buffer.drawString(200, 720, institution_name)

    # Add title
    buffer.setFont("Helvetica-Bold", 16)
    buffer.drawString(100, 680, "Registration Clearance Fee Slip")

    # Add user details
    buffer.setFont("Helvetica", 12)
    buffer.drawString(50, 650, f"Student Name: {full_name}")
    buffer.drawString(50, 630, f"Date: {today}")

    # Document Status Section
    buffer.setFont("Helvetica-Bold", 14)
    buffer.drawString(50, 600, "Document Status:")

    # Check document statuses and add them to the PDF
    document_statuses = {
        'JAMB Admission Letter': get_document_status(registration.jamb_admission_letter),
        'School Admission Letter': get_document_status(registration.school_admission_letter),
        'JAMB Result Slip': get_document_status(registration.jamb_result_slip),
        'O\'Level Result': get_document_status(registration.o_level_result),
        'Medical Examination Form': get_document_status(registration.medical_examination_form),
        'Parent Letter of Undertaking': get_document_status(registration.letter_of_undertaking_parent),
        'Guarantor Letter of Undertaking': get_document_status(registration.letter_of_undertaking_guarantor),
        'Birth Certificate': get_document_status(registration.birth_certificate),
        'Local Government Certification': get_document_status(registration.local_government_certification),
        'Bio-Data': get_document_status(registration.bio_data),
    }

    y_position = 570
    for document, status in document_statuses.items():
        buffer.drawString(50, y_position, f"- {document}: {status}")
        y_position -= 15

    # Draw a separator line
    buffer.line(50, 550, 550, 550)

    # Add footer text
    buffer.setFont("Helvetica", 10)
    buffer.drawString(50, 530, f"This is a computer-generated document and does not require a signature.")

    buffer.save()
    return response


def get_document_status(document_instance):
    if document_instance:
        return "Submitted"
    else:
        return "Missing"


