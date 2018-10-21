"""frontend URL Configuration

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
import requests
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import JsonResponse
from django.urls import path


def home(request: WSGIRequest):
    for key, value in request.META.items():
        if any(needle in key for needle in ('b3', 'trace')):
            print('{}: {}'.format(key, value))
    response = requests.get(
        'https://query.yahooapis.com/v1/public/yql?q=select%20item.condition.text%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22dallas%2C%20tx%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys')
    response.raise_for_status()
    weather = response.json()
    return JsonResponse(dict(data=weather))


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
]
