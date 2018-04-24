"""
Institution : DTU
Course      : Master Thesis Project
Date        : 20-Jan-2018
Author      : Jaime Liew - S141777
Email       : Jaimeliew1@gmail.com
Description : A Python wrapper class for interfacing HAWC2 simulations via
              TCP. The HAWC2 simulation requires a TCP DLL.
"""

import socket
import numpy as np
import time

class HAWC2_TCP(object):
    def __init__(self, PORT=None, TCP_IP='127.0.0.1', connectAttempts=20):
        #Makes a TCP client
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if PORT is not None:
            #Make TCP connection if a port number is provided.
            self.connect(PORT, TCP_IP, connectAttempts)

    def connect(self, PORT, TCP_IP='127.0.0.1', connectAttempts=20, printStatus=True):
        #If no port number is provided in object initiation, this function can
        #be used to connect to a port.
        #Attempts to connect to HAWC2 connectAttempts many times before
        #raising a ConnectionRefusedError.
        #prints connection status to console if printStatus is True.
        Connected = False
        Attempts = 0
        while not Connected:
            if Attempts >= connectAttempts:
                raise ConnectionRefusedError('Cannot connect to HAWC2.')
                break
            try:
                self.socket.connect((TCP_IP, PORT))
                Connected = True
                if printStatus:
                    print('HAWC2 Connected.')
            except ConnectionRefusedError:
                Attempts += 1
                if printStatus:
                    print('HAWC2 Not ready. Try again...')
                time.sleep(1)


    def getMessage(self, Nkeep=None, keys=None, BUFFER_SIZE=1024):
        # Waits until a message is received from HAWC2, and returns the
        # message in a numpy array. Keeps the first Nkeep elements. if Nkeep
        # is not provided, all elements are returned.
        #If a list of keys is provided, returns the data in a dictionary
        # instead of an numpy.ndarray.


        message = self.socket.recv(BUFFER_SIZE)
        data = message.decode('utf-8')
        if Nkeep is not None:
            data = np.array([float(x) for x in data.split(';')[1:Nkeep+1]])
        else:
            data = np.array([float(x) for x in data.split(';')[1:]])

        if keys is not None:
            assert len(keys) == Nkeep
            data = dict(zip(keys,data))

        return data

    def sendMessage(self, message):
        #Encodes and sends a message to HAWC2. message should be either a list
        #or a numpy array.
        out = ''.join(['{:2.8f};'.format(x) for x in message]) + '*'
        out = out.encode('utf-8')
        self.socket.send(out)

    def close(self):
        self.socket.close()