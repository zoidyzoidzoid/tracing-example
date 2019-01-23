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
from django.contrib import admin, auth
from django.contrib.auth.models import AnonymousUser
from django.http.response import JsonResponse
from django.urls import path
from opencensus.trace import execution_context


def home(request):
    _tracer = execution_context.get_opencensus_tracer()
    if _tracer is not None:
        headers = _tracer.propagator.to_headers(_tracer.span_context)
    else:
        headers = {}
    print(headers)
    response = requests.get('http://127.0.0.1:8081/', headers=headers)
    response.raise_for_status()
    weather = response.json()
    if isinstance(request.user, AnonymousUser):
        user = 'Not logged in.'
    else:
        user = request.user.get_username()
    users_count = auth.get_user_model().objects.count()
    return JsonResponse(dict(
        message='Hello, World!',
        weather_weather=weather['weather'][0],
        weather_location=weather['name'],
        user=user,
        users_count=users_count,
    ))


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
]
