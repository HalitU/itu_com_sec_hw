from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import numpy as np
import ast

class TestView(View):
    def generate_key_pair(self):
        rand_num_generator = Random.new().read
        pb_pr_key = RSA.generate(1024, rand_num_generator) # public-private key pair generation
        return pb_pr_key

    def get(self, request, *args, **kwargs):
        return render(request, 'index2.html', {})

    def post(self, request, *args, **kwargs):
        print("Kek")
        print(request.POST['haha'])
        print(request.POST['hidden'])
        b64_data = request.POST['hidden']
        cleared_data = b64_data[22:]
        
        print(len(cleared_data) % 4)
        pb_pr_key = self.generate_key_pair()
        pb_key = pb_pr_key.publickey() # separate public key to use in encryption
        print(pb_key)
        # Image encryption/decryption
        encrypted_data = pb_key.encrypt(base64.b64decode(cleared_data), 32)
        print(encrypted_data)
        fh = open("imageToSave.txt", "w")
        fh.write(str(encrypted_data))
        fh.close()

        f = open ("imageToSave.txt", 'r')
        data = f.read()
        print(data)
        decrypted_data = pb_pr_key.decrypt(ast.literal_eval(str(data)))
        print("------------------------------------------------")
        print(decrypted_data)
        print("------------------------------------------------")
        print(base64.b64encode(decrypted_data))
        print("------------------------------------------------")
        fh = open("imageToSave.png", "wb")
        fh.write(decrypted_data)
        fh.close()
        '''
        # Message encryption/decryption
        encrypted_data = pb_key.encrypt(base64.b64encode(b'hello'), 32)
        print(encrypted_data)
        fh = open("imageToSave.txt", "w")
        fh.write(str(encrypted_data))
        fh.close()

        f = open ("imageToSave.txt", 'r')
        data = f.read()
        print(data)
        decrypted_data = pb_pr_key.decrypt(ast.literal_eval(str(data)))
        print("------------------------------------------------")
        print(decrypted_data)
        print("------------------------------------------------")
        print(base64.b64decode(decrypted_data))
        '''
        '''
        # Save file to system just for checking
        fh = open("imageToSave.png", "wb")
        fh.write(base64.b64decode(cleared_data))
        fh.close()
        '''
        return render(request, 'index2.html', {})
