from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from core.models import Section



# class GetLanding(TemplateView):
#     template_name = 'landing.html'

class GetLanding(View):
    def get(self, request, *args, **kwargs):
        sections = Section.objects.all()
        context = {
            'sections': sections
        }
        template_name = 'landing.html'
        return render(request, template_name, context)