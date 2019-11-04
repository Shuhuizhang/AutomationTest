"""HaizolTestAuto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url


from cases.views import IndexView, HomeView, CaseListView, PlanListView, SaveCaseView, OptionlistView, \
    CreateTestPlanView, RunPlanView, DelPlanView, PlanDetailView, TestReportView, SaveReportView

urlpatterns = [
    url(r'^index$', IndexView.as_view(), name='index'),
    url(r'^home$', HomeView.as_view(), name='home'),
    url(r'^case_list/(?P<page>\d+)$', CaseListView.as_view(), name='case_list'),
    url(r'^plan_list/(?P<page>\d+)$', PlanListView.as_view(), name='plan_list'),
    url(r'^save$', SaveCaseView.as_view(), name='save'),
    url(r'^option_list$', OptionlistView.as_view(), name='option'),
    url(r'^create_plan$', CreateTestPlanView.as_view(), name='create_plan'),
    url(r'^run_plan/(?P<plan_id>\d+)$', RunPlanView.as_view(), name='run_plan'),
    url(r'^del_plan$', DelPlanView.as_view(), name='del_plan'),
    url(r'^plan_detail$', PlanDetailView.as_view(), name='plan_detail'),
    url(r'^report_list/(?P<page>\d+)$', TestReportView.as_view(), name='report_list'),
    url(r'^create_report$', SaveReportView.as_view(), name='save_report'),

]
