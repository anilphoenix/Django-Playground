from django.contrib import admin

from .models import Question, Choice, StepCount, MonthlyWeatherByCity, ReqsCount

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(StepCount)
admin.site.register(MonthlyWeatherByCity)
admin.site.register(ReqsCount)
