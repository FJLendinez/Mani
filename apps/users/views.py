from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.users.forms import UserUpdateForm, UserChangePasswordForm


# Create your views here.
def login_view(request):
    if request.method == "GET":
        return render(request, "pages/users/login.html")
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
    return redirect(request.GET.get("next") or "/")


@login_required()
def user_settings(request):
    if request.method == "POST":
        user_update_form = UserUpdateForm(data=request.POST, instance=request.user)
        if user_update_form.is_valid():
            user_update_form.save()
            messages.add_message(request, messages.SUCCESS, "Guardado con éxito")
        else:
            messages.add_message(request, messages.ERROR, user_update_form.errors)
    else:
        user_update_form = UserUpdateForm(instance=request.user)
    context = {
        'user_update_form': user_update_form,
        'change_password_form': UserChangePasswordForm()
    }
    return render(request, "pages/users/settings.html", context)


@login_required()
def change_password(request):
    if request.method == "POST":
        change_password_form = UserChangePasswordForm(data=request.POST)
        if change_password_form.is_valid():
            request.user.set_password(change_password_form.cleaned_data['password'])
            request.user.save()
        else:
            messages.add_message(request, messages.ERROR, change_password_form.non_field_errors())
    else:
        change_password_form = UserChangePasswordForm()
    context = {
        'user_update_form': UserUpdateForm(instance=request.user),
        'change_password_form': change_password_form
    }
    return render(request, "pages/users/settings.html", context)
