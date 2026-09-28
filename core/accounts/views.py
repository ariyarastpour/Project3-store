from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.views.generic import CreateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from .models import ActivationToken
from .forms import *
from .api.v1.utils import send_activation_email


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'accounts/signup.html'
    form_class = RegistrationForm
    success_message = 'ثبت نام کاربر با موفقیت انجام شد!'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        user.is_active = True
        user.save()
        login(self.request, user)

        return response
    
class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = CustomAuthenticationForm
    success_message = "کاربر با موفقیت وارد شد!"
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    pass


class SendVerificationView(LoginRequiredMixin, View):
    
    def post(self, request):
        user = request.user
        
        if user.is_verified:
            messages.info(request, "ایمیل شما قبلاً تایید شده است.")
            return redirect('website:home')
        
        ActivationToken.objects.filter(user=user).delete()
        token_obj = ActivationToken.objects.create(user=user)
        send_activation_email(user, token_obj, request)
        
        messages.success(request, "کد تایید به ایمیل شما ارسال شد.")
        
        return redirect('verify-code')


class VerifyCodePageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/verification_email/verify_code.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_verified:
            messages.info(request, "ایمیل شما قبلاً تایید شده است.")
            return redirect('website:home')
        return super().get(request, *args, **kwargs)


class VerifyEmailView(LoginRequiredMixin, View):
    
    def post(self, request):
        user = request.user
        code = request.POST.get('code', '').strip()
        
        if user.is_verified:
            messages.info(request, "ایمیل شما قبلاً تایید شده است.")
            return redirect('website:home')
        
        if not code or len(code) != 6:
            messages.error(request, "کد باید ۶ رقم باشد.")
            return redirect('verify-code')
        
        token_obj = ActivationToken.objects.filter(user=user, otp_code=code).first()

        if not token_obj:
            messages.error(request, "کد وارد شده صحیح نیست.")
            return redirect('verify-code')
        
        if token_obj.is_expired():
            token_obj.delete()
            messages.error(request, "کد منقضی شده است. دوباره درخواست بده.")
            return redirect('verify-code')
        
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        token_obj.delete()
        
        messages.success(request, "✅ ایمیل شما با موفقیت تایید شد!")
        return redirect('website:home')