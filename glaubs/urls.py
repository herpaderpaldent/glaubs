"""glaubs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url

from rest_framework_nested import routers

from glaubs.views import IndexView

from municipalities.views import MunicipalityViewSet, SearchMunicipality, \
    PrimaryMunicipality, RelatedMunicipalities
from mailings.views import MailingViewSet, MailingsMark, MailingMaxNumber, \
    MailingsRemider, MailingsMunicipalityRemider, MailingSearch, PDFView, \
    MailingStatistics

router = routers.SimpleRouter()
router.register(r'municipalities', MunicipalityViewSet)

domains_router = \
    routers.NestedSimpleRouter(
        router, r'municipalities', lookup='municipality')
domains_router.register(r'mailings', MailingViewSet, base_name='mailings')

urlpatterns = [
    url(r'^api/v1/municipalities/primary$', PrimaryMunicipality.as_view()),
    url(r'^api/v1/municipalities/related$', RelatedMunicipalities.as_view()),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(domains_router.urls)),
    url(r'^api/v1/municipalities/search$', SearchMunicipality.as_view()),
    url(r'^api/v1/mailings/max_to_number$', MailingMaxNumber.as_view()),
    url(r'^api/v1/mailings/pdf$', PDFView.as_view()),
    url(r'^api/v1/mailings/search$', MailingSearch.as_view()),
    url(r'^api/v1/mailings/reminders$', MailingsRemider.as_view()),
    url(r'^api/v1/mailings/statistics$', MailingStatistics.as_view()),
    url(
        r'^api/v1/mailings/reminders/by_municipality$',
        MailingsMunicipalityRemider.as_view()),
    url(
        r'^api/v1/municipalities/(?P<municipality_id>[0-9]+)/mailings/mark$',
        MailingsMark.as_view()),
    url(r'^.*$', IndexView.as_view(), name='index'),
]
