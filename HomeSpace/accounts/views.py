from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.http import HttpResponse
from .models import Member
from django.contrib.auth.models import User

# Create your views here.

def SignUp(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data.get('first_name')
            lname = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            number = form.cleaned_data.get('contact_number')
            p1 = form.cleaned_data.get('password1')
            p2 = form.cleaned_data.get('password2')
            username = form.cleaned_data.get('username')
            user = User.objects.create_user(username=username, first_name = fname, last_name = lname, password=p1, email=email)
            user.save()
            member = Member.objects.create(user = User, contact_number=number)
            member.save()
            return redirect('accounts:login')

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


