from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import ContactForm
from django.urls import reverse_lazy

class IndexView(TemplateView):
    template_name = "website/index.html"

class AboutView(TemplateView):
    template_name = "website/about.html"

# شرط لاگین
class ContactView(FormView):
    template_name = "website/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("website:home")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
