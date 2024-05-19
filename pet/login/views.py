from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from .forms import SignUpForm, SignInForm, ForgotPasswordForm
from datetime import timedelta
from .models import UserProfile

def email_sent(request):
    return render(request, 'email_sent.html')

def account_activated(request):
    return render(request, 'account_activated.html')

def activation_failed(request):
    return render(request, 'activation_failed.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            UserProfile.objects.create(
                user=user,
                **form.cleaned_data
            )

            send_confirmation_email(request, user)
            return redirect('email_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def send_confirmation_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'

    expiration_time = timezone.now() + timedelta(minutes=30)
    protocol = 'https' if request.is_secure() else 'http'

    message = render_to_string('confirmation_email.html', {
        'user': user,
        'protocol': protocol,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'expiration_time': expiration_time.timestamp(),
    })

    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"
    email.send()

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        expiration_time = request.GET.get('expiration_time')

        if expiration_time:
            expiration_time = float(expiration_time)
            if timezone.now().timestamp() > expiration_time:
                return redirect('link_expired')

        user.is_active = True
        user.save()
        return redirect('account_activated')
    else:
        return redirect('activation_failed')

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('home')

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = get_user_model().objects.get(email=email)
                form = PasswordResetForm({'email': email})
                if form.is_valid():
                    form.save()
                return redirect('home')
            except get_user_model().DoesNotExist:
                pass
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})

def home(request):
    return render(request, 'home1.html')
