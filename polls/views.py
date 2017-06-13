from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from chartit import DataPool, Chart
from datetime import datetime, date

from .models import Question, Choice, MonthlyWeatherByCity, ReqsCount, Project, UserProject, Setting, Page

from .utilities import Utilities

import subprocess, os

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

def site_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/chart/')
    else:
        return login(request)

@login_required
def dash1(request):
    return render_to_response('dashboard/_Dashboard.html')

@login_required
def dash(request):
    project_owners = {}
    for project in Project.objects.filter(deleted=False):
        project_owners[project.name] = project.userproject_set.first().owner.username
    return render_to_response('dashboard/dashboard.html', {'user': request.user,
                                                           'project_owners': project_owners,
                                                           'projects': Project.objects.filter(deleted=False),})

@login_required
def add_project(request):
    if request.method == 'POST':
        project = Project.objects.create(name=request.POST['name'])
        userProject = UserProject.objects.create(owner=request.user, project=project)
        # if Project.objects.filter(name=request.POST['name']).count() == 0:
        #     project = Project.objects.create(name=request.POST['name'])
        #     userProject = UserProject.objects.create(owner=request.user, project=project)
        # else:

        return HttpResponseRedirect(reverse('polls:home'))

    else:
        # return render_to_response('dashboard/form_new_project.html', {'user': request.user})
        return render(request, 'dashboard/form_new_project.html', {'user': request.user, 'user_projects': Project.objects.filter(userproject__owner=request.user)})

@login_required
def delete_project(request, project_id):
    if request.user.is_authenticated:
        project = Project.objects.get(id = project_id)
        project.deleted = True
        project.save()
    return HttpResponseRedirect(reverse('polls:home'))

@login_required
def project_home(request, project_id):
    need_update = False
    last_update = Setting.objects.filter(option_name='last_update').first()
    today = date.today()

    if last_update is None:
        Setting.objects.create(option_name='last_update', option_value=today.strftime('%d %B %Y'), option_meta='')
        need_update = True
    else:
        last_date = datetime.strptime(last_update.option_value, '%d %B %Y')
        if today > last_date.date():
            need_update = True
            last_update.option_value = today.strftime('%d %B %Y')
            last_update.save()

    # if need_update:
        subprocess.Popen('C:/xampp/htdocs/netpage/dxl/DOORSGenReportAndPlot.cmd')

    for req in ReqsCount.objects.all():
        req.page = Page.objects.get(name="Page 1-Paul")
        req.save()

    # with open("//dmaid0048/xampp/htdocs/projectsdashboard/netpage/contents/projects/Paul/ReqsCountQuery_plot", 'rb') as f:
    # with open("ReqsCountQuery_plot",'rb') as f:
    with open("C:/xampp/htdocs/netpage/contents/projects/Paul/ReqsCountQuery_plot",'rb') as f:
        offset = -24
        readline = -1
        f.seek(offset, 2)
        line = f.readlines()[readline].decode()
        info = line.split()
        item_date = datetime.strptime(info[0] + ' ' + info[1] + ' ' + info[2], '%d %B %Y')

        while True:
            if ReqsCount.objects.filter(date=item_date, total=info[3], completed=info[4]).count() < 1:
                ReqsCount.objects.create(date=item_date, total=info[3], completed=info[4])
            offset = offset-26
            readline = readline-1
            try:
                f.seek(offset, 2)
                line = f.readlines()[readline].decode()
                info = line.split()
                item_date = datetime.strptime(info[0] + ' ' + info[1] + ' ' + info[2], '%d %B %Y')
            except OSError:
                break

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

    return render_to_response('dashboard/project_home.html', {'weatherCharts': [ccht2],
                                                           'user': request.user,
                                                           'user_projects': Project.objects.filter(userproject__owner=request.user),
                                                           'projects': Project.objects.filter(deleted=False),})

@login_required
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
    # return render_to_response('polls/dashboard.html', {'weatherCharts': [lcht, acht,
    #                                                                     # Hpcht, Bpcht,
    #                                                                     ccht1, ccht2]})
