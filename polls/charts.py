from django_google_charts import charts
from .models import StepCount

class StepChart(charts.Chart):
    chart_slug = 'steps_chart'
    columns = (
        ('datetime', "Date"),
        ('number', "Steps"),
    )

    def get_data(self):
        return StepCount.objects.values_list('date', 'count')
