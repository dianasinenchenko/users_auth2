from django.shortcuts import render, redirect
from django.views import generic
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.contrib.auth import login
from users_auth2.authentication.forms import SignUpForm
from users_auth2.authentication.tokens import account_activation_token


def home(request):
    return render(request, 'home.html')


def base(request):
    return render(request, 'base.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            request.session['uidb64'] = user.pk
            return redirect('login')
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

        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


class UserListView(generic.ListView):
    model = User
    paginate_by = 10
    template_name = 'user_list.html'

