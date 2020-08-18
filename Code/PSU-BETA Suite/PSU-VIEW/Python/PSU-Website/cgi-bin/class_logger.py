'''
Author: Rachel Alcraft
Date: 27/6/20
Description: This enables logging to the cgi screen before print
'''

class logger:
    def __init__(self,isDebug):
        self.debug = isDebug
    def log(self, message):
        if self.debug:
            print(message + '<br/>')
