import datetime

from django.db import models
from django.utils import timezone

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

class ReqsCount(models.Model):
    def __str__(self):
        return str(self.date) + " (" + str(self.completed) + " / " + str(self.total) + ")"

    date = models.DateField()
    total = models.IntegerField()
    completed = models.IntegerField()
