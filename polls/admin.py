from django.contrib import admin

from .models import Question, Choice, StepCount, MonthlyWeatherByCity, ReqsCount, Project, UserProject

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(StepCount)
admin.site.register(MonthlyWeatherByCity)
admin.site.register(ReqsCount)
admin.site.register(Project)
admin.site.register(UserProject)
