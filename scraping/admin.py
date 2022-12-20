from django.contrib import admin
from .models import City, Language, Vacancy, Error, Url


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_filter = ['city', 'language']


admin.site.register(City)
admin.site.register(Language)
admin.site.register(Error)
admin.site.register(Url)


