from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.urls import reverse
from django.views import generic
from chartit import DataPool, Chart

from .models import Question, Choice, MonthlyWeatherByCity, ReqsCount

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def monthname(month_num):
    names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
             7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    return names[month_num]

def weather_chart_view(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
           series=
            [{'options': {
               'source': MonthlyWeatherByCity.objects.all()},
              'terms': [
                'month',
                'houston_temp',
                'boston_temp',
                'newyork_temp']}
             ])

    reqsCountData = \
        DataPool(
           series=
            [{'options': {
               'source': ReqsCount.objects.all()},
              'terms': [
                'date',
                'total',
                'completed']}
             ])

    #Step 2: Create the Chart object
    lcht = Chart(
            datasource=reqsCountData,
            series_options=
              [{'options': {
                  'type': 'line'},
                'terms': {
                  'date': [
                    'total',
                    'completed']
                  }}],
            chart_options=
              {'title': {
                   'text': 'ReqsCountQuery - Line Chart'},
                'xAxis': {
                    'title': {
                       'text': 'Days'}},
                'yAxis': {
                  'title': {
                      'text': 'Total/Completed'}}})

    acht = Chart(
            datasource=reqsCountData,
            series_options=
              [{'options': {
                  'type': 'area'},
                'terms': {
                  'date': [
                    'total',
                    'completed']
                  }}],
            chart_options=
              {'title': {
                   'text': 'ReqsCountQuery - Area Chart'},
                'xAxis': {
                    'title': {
                       'text': 'Days'}},
                'yAxis': {
                  'title': {
                      'text': 'Total/Completed'}}})

    Hpcht = Chart(
            datasource=weatherdata,
            series_options=
              [{'options': {
                  'type': 'pie'},
                'terms':{
                  'month': [
                    'houston_temp']
                  }}],
            chart_options=
              {'title': {
                   'text': 'Houston - Pie Chart'},
                'xAxis': {
                    'title': {
                       'text': 'Month'}},
                'yAxis': {
                  'title': {
                      'text': 'Temperature'}}
              },
            x_sortf_mapf_mts=(None, monthname, False))

    Bpcht = Chart(
            datasource = weatherdata,
            series_options =
              [{'options':{
                  'type': 'pie',
                  'stacking': False},
                'terms':{
                  'month': [
                    'boston_temp']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Boston - Pie Chart'},
                'xAxis': {
                    'title': {
                       'text': 'Month'}},
                'yAxis': {
                  'title': {
                      'text': 'Temperature'}}
              })

    ccht1 = Chart(
            datasource = reqsCountData,
            series_options =
              [{'options':{
                  'type': 'column',
                  'stacking': True},
                'terms':{
                  'date': [
                    'total',
                    'completed']
                  }}],
            chart_options =
              {
                  'title': {
                   'text': 'ReqsCountQuery - Column Chart'},
                  'xAxis': {
                      'title': {
                          'text': 'Days'}},
                  'yAxis': {
                      'title': {
                          'text': 'Total/Completed'}}
              }
        # x_sortf_mapf_mts=(None, monthname, False)
    )

    ccht2 = Chart(
        datasource=reqsCountData,
        series_options=[{
            'options': {
                'type': 'column',
                'stacking': True,
                'colors': ['#339966', '#ff80bf', '#3366cc'],
                'stack': 0
            },
            'terms': {
                'date': [
                    'total',
                    {
                        'completed': {
                            'stack': 1
                        }
                    },
                ]
            }
        }],
        chart_options=
              {
                  'title': {
                   'text': 'ReqsCountQuery - Column Chart with multiple stacks'},
                  'xAxis': {
                      'title': {
                          'text': 'Days'}},
                  'yAxis': {
                      'title': {
                          'text': 'Total/Completed'}}
              }
        # x_sortf_mapf_mts=(None, monthname, False)
    )

    #Step 3: Send the chart object to the template.
    return render_to_response('polls/template.html', {'weatherCharts': [lcht, acht,
                                                                        # Hpcht, Bpcht,
                                                                        ccht1, ccht2]})
