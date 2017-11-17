from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

import base64
import numpy as np

class TestView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index2.html', {})

    def post(self, request, *args, **kwargs):
        print("Kek")
        print(request.POST['haha'])
        print(request.POST['hidden'])
        b64_data = request.POST['hidden']
        cleared_data = b64_data[22:]
        print(len(cleared_data) % 4)
        # Save file to system just for checking
        fh = open("imageToSave.png", "wb")
        fh.write(base64.b64decode(cleared_data))
        fh.close()
        return render(request, 'index2.html', {})
