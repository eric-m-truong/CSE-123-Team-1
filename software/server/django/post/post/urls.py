"""post URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
# https://docs.djangoproject.com/en/4.0/ref/request-response/
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import engines, Context, Template


form = """
<form action="post" method="post">
{% csrf_token %}
<input type="hidden" name="plug" value="test">
<input type="submit" value="do it">
</form>
<form action="post" method="post">
{% csrf_token %}
<input type="submit" value="don't do it">
</form>
"""

t = engines['django'].from_string(form)

def post(request):
  """ request should specify which plug to toggle """
  if request.method == 'POST':
    try:
      plug = request.POST['plug']
    except KeyError:
      return HttpResponseBadRequest('request must include plug name')
    print(plug)
  return HttpResponse(status=204)

def index(request):
  rt = t.render({}, request)
  return HttpResponse(rt)

urlpatterns = [
  path('', index),
  path('post', post),
]
