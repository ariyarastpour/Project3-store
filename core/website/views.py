from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import ContactForm
from .models import *
from django.urls import reverse_lazy

class IndexView(TemplateView):
    template_name = "website/index.html"


class AboutView(TemplateView):
    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aboutsetting'] = AboutSetting.objects.first()
        return context


class ContactView(FormView):
    model = ContactSetting
    template_name = "website/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("website:home")

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['email'] = self.request.user.email

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contactsetting'] = ContactSetting.objects.first()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class PrivacyView(TemplateView):
    template_name = 'website/privacy-policy.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            context['privacy_setting'] = PrivacySetting.objects.first()
        except PrivacySetting.DoesNotExist:
            context['privacy_setting'] = None
        
        context['privacy_sections'] = PrivacySection.objects.filter(
            is_active=True
        ).order_by('order')
        
        return context
    

class TermsView(TemplateView):    
    template_name = 'website/terms.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['config'] = TermsConfig.get_solo()
        context['sections'] = TermsSection.objects.filter(is_active=True)
        return context