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

        # Getting the image data
        b64_data = request.POST['hidden']
        # Splitting the initial unnecessary data
        cleared_data = b64_data[22:]
        # Data needs to be a multiply of 4
        print(len(cleared_data) % 4)
        # Generate keys
        pb_pr_key = self.generate_key_pair()
        pb_key = pb_pr_key.publickey() # separate public key to use in encryption
        print(pb_key)

        # ENCRYPTION PART
        decoded_data = base64.b64decode(cleared_data)
        # Split data into 128 character parts
        splitted_cleared_data = [cleared_data[i:i+128] for i in range(0, len(cleared_data), 128)]
        # Encrypt all the data in array
        splitted_encrypt_data = [pb_key.encrypt(str(i), 32) for i in splitted_cleared_data]
        # Write encrypted array to file
        fh = open("imageToSave.txt", "w")
        for item in splitted_encrypt_data:
            fh.write("%s \n" % str(item))
        fh.close()
        # If you want to see the image file
        fh = open("imageToSave.png", "wb")
        fh.write(base64.b64decode(cleared_data))
        fh.close()
        # DECODING PART
        # Read crypted data from the file
        with open("imageToSave.txt") as f:
            content = f.readlines()
        # Divide it into the array
        content = [x.strip() for x in content]
        # Decode the data
        splitted_decrypt_data = [pb_pr_key.decrypt(ast.literal_eval(str(i))) for i in content]

        # Checking initial and encoded data to be equal
        is_equal = True
        for i in range(0, len(splitted_cleared_data)):
            if str(splitted_cleared_data[i]) != splitted_decrypt_data[i]:
                is_equal = False
        print is_equal 

        return render(request, 'index2.html', {})
