import time

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from .models import Service
import os
import sys


sys.path.append(os.path.abspath('../'))
print(sys.path)
print('-------------------------------')
from hcheck import Service as Srv

# Create your views here.
def index(request):
    services = Service.objects.all()
    return render(request, 'healthcheck/index.html', {'services': services})


class CheckStatusView(View):
    def get(self, request, *args, **kwargs):
        # service = Srv(self.kwargs.get('name'))
        # print(service.status_humanized())
        # print(service.status1)
        # print(service.status1)
        # print('sleeeping for 3 sec')
        resp = {
            'status': 'OK',
            'message': 'received'
        }
        # time.sleep(3)
        # return JsonResponse(resp)

    def post(self):
        print('post called')
        return HttpResponse("i got u post ")

