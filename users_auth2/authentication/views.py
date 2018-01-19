from django.shortcuts import render, redirect
from users_auth2.authentication.forms import SignUpForm
from users_auth2.authentication.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from django.contrib.auth import login


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            request.session['uidb64'] = user.pk

            return redirect('user_page')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)

       # return redirect('')
    else:
        return render(request, 'account_activation_invalid.html')


def user_page(request):
    uidb64 = request.session.get('uidb64')
    try:

        user = User.objects.get(pk=uidb64)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return render(
        request,
        'user_page.html',
        context={'user':user}
    )


def users(request):

    try:

        user = User.objects.count()
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return render(
        request,
        'user_list.html',
        context={'user': user}
    )
