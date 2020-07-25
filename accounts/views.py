from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from .forms import SignUpForm



def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("products:product-list")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            args = {'form': form}
            return render(request, 'registration/register.html', args)

    else:
        form = SignUpForm()
        args = {'form': form}
        return render(request, 'registration/register.html', args)
