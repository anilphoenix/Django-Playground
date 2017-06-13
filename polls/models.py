import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class StepCount(models.Model):
    def __str__(self):
        return str(self.count) + "(" + datetime.date.strftime(self.date, '%Y-%m-%d') + ")"

    date = models.DateField('date')
    count = models.IntegerField(default=0)

class MonthlyWeatherByCity(models.Model):
    def __str__(self):
        return str(self.month) + "(H: " + str(self.houston_temp) + ", B: " + str(self.boston_temp) + ", N: " + str(self.newyork_temp) + ")"

    month = models.IntegerField()
    boston_temp = models.DecimalField(max_digits=5, decimal_places=1)
    houston_temp = models.DecimalField(max_digits=5, decimal_places=1)
    newyork_temp = models.DecimalField(max_digits=5, decimal_places=1)

class Project(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50)
    deleted = models.BooleanField(default=False)

class UserProject(models.Model):
    def __str__(self):
        return self.project.name + "(" + self.owner.username + ")"

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Page(models.Model):
    def __str__(self):
        return self.name + "-" + str(self.project.name)

    name = models.CharField(max_length=50)
    project = models.ForeignKey(Project)

class ReqsCount(models.Model):
    def __str__(self):
        return str(self.date) + " (" + str(self.completed) + " / " + str(self.total) + ")" #+ " Page:" + str(self.page.name)

    date = models.DateField()
    total = models.IntegerField()
    completed = models.IntegerField()
    page = models.ForeignKey(Page)

class Setting(models.Model):
    def __str__(self):
        return self.option_name + "=" + str(self.option_value) + "(" + str(self.option_meta) + ")"

    option_name = models.CharField(max_length = 1000)
    option_value = models.CharField(max_length = 25000)
    option_meta = models.CharField(max_length = 1000, blank=True)
