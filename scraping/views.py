from django.shortcuts import render
from django.views.generic import ListView
from .models import Vacancy
from .forms import FindForm


class ListHomeView(ListView):
    model = Vacancy
    template_name = 'scraping/home.html'
    queryset = Vacancy.objects.all()
    # context_object_name = 'object_list'

    def get(self, request):
        form = FindForm()
        city = request.GET.get('city')
        language = request.GET.get('language')

        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            elif language:
                _filter['language__slug'] = language

            qs = Vacancy.objects.filter(**_filter)
        return render(request, 'scraping/home.html', {'object_search': qs, 'form': form})