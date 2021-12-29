import json
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet.protocol import Protocol

class Call:
    def __init__(self,id):
        self.id = id

class Operator:
    def __init__(self,id):
        self.id=id
        self.status = "AVAILABLE"
        self.call = None
        self.callTimeout = None
    
    def ring(self, call,proto):
        message = "Call {callId} ringing for operator {operatorId}".format(callId= call.id, operatorId= self.id)
        self.status = "RINGING"
        self.call = call
        self.callTimeout = reactor.callLater(10, self.timeout, proto) 
        return  message

    def answer(self):
        message ="Call {callId} answered by operator {operatorId}".format(callId=self.call.id, operatorId=self.id)
        self.status = "BUSY"
        self.callTimeout.cancel()
        self.callTimeout = None
        return message

    def reject(self):
        rejecCall = self.call
        message ="Call {callId} rejected by operator {operatorId}".format(callId=self.call.id, operatorId=self.id)
        self.status = "AVAILABLE"
        self.call = None
        self.callTimeout.cancel()
        self.callTimeout = None
        return rejecCall, message
    
    def hangup(self):
        if self.status == "RINGING":
            message = "Call {callId} missed".format(callId =self.call.id)
        if self.status == "BUSY":
            message = "Call {callId} finished and operator {operatorId} available".format(callId = self.call.id, operatorId = self.id)
        self.status = "AVAILABLE"
        self.call = None
        self.callTimeout = None
        return message  

    def timeout(self,proto):
        message = ["Call {callId} ignored by operator {operatorId}".format(callId= self.call.id, operatorId = self.id)]
        output = json.dumps({'line' : message}).encode('utf-8')
        self.status = "AVAILABLE"
        self.call = None
        self.callTimeout = None
        