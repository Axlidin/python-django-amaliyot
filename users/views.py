from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserCreateForm, UpdateProfileForm


class RegisterView(View):

    def get(self, request):
        create_form = UserCreateForm()
        context = {
            'form': create_form
        }
        return render(request, 'users/register.html', context=context)

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')

        else:
            context = {
                'form': create_form
            }
            return render(request, 'users/register.html', context=context)

class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()

        return render(request, 'users/login.html', {'login_form': login_form})
    def post(self, request):
        # print(request.POST['username'], request.POST['password'])
        # login_form = CustomUserLoginForm(data=request.POST)
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You have been successfuly login.")
            return redirect('posts:post_list')
        else:
            return render(request,
                          'users/login.html',
                          {'login_form': login_form})

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        # if not request.user.is_authenticated:
        #     return redirect('users:login')
        return render(request, 'users/profile.html', {"user": request.user})

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('landing_page')

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        CustomUser_update_form = UpdateProfileForm(instance=request.user)
        return render(request, 'users/profile_update.html',
                      {'form': CustomUser_update_form})

    def post(self, request):
        CustomUser_update_form = UpdateProfileForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
            )
        if CustomUser_update_form.is_valid():
            CustomUser_update_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('users:profile')
        else:
            return render(request, 'users/profile_update.html',
                          {'form': CustomUser_update_form})
