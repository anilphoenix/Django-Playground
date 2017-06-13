from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/dash/'), name='home'),
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^chart/$', views.weather_chart_view, name='chart'),
    url(r'^dash1/$', views.dash1, name='dash1'),
    url(r'^dash/$', views.dash, name='dash'),
    url(r'^dash/add_project/$', views.add_project, name='add_project'),
    url(r'^(?P<project_id>[0-9]+)/delete/$', views.delete_project, name='delete_project'),
    url(r'^dash/project/(?P<project_id>[0-9]+)', views.project_home, name='project_home'),
    # url(r'^dash/handle_add_project/$', views.handle_add_project, name='handle_add_project'),
]