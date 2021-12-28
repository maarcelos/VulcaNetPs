from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.internet.protocol import Factory
import json
import classes


class QOTD(Protocol):
    def __init__(self):
        self.operators = []
        self.operators.extend([classes.Operator("A"),classes.Operator("B")])
        self.callsQ = []
        super().__init__()
        
    def dataReceived(self, data):
        message = self.qManager(data)
        self.transport.write(message)
    
    def findAvailable(self):
        for i in range(len(self.operators)):
            if self.operators[i].status == "AVAILABLE":
                return i
        return None
    
    def qManager(self,data):
        data = json.loads(data.decode('utf-8'))
        command = data["command"]
        commandId = data["id"]
        output = []
        if command == "call":
            call = classes.Call(commandId)
            self.callsQ.append(call)
            output.append("Call {callId} received".format(callId =commandId))
            if self.findAvailable() == None:
                output.append("Call {callId} waiting in queue".format(callId=commandId))
        if command == "answer":
            for i in range(len(self.operators)):
                if self.operators[i].id == commandId:
                    mes = self.operators[i].answer()
                    output.append(mes)
        if command == "reject":
            for i in range(len(self.operators)):
                if self.operators[i].id == commandId:
                    rejectCall,mes = self.operators[i].reject()
                    output.append(mes)
                    self.callsQ.insert(0, rejectCall)
        if command == "hangup":
            for i in range(len(self.callsQ)): #caso esteja na queue
                if self.callsQ[i].id == commandId:
                    output.append("Call {callId} missed".format(callId = self.callsQ[i].id))
                    self.callsQ.remove(self.callsQ[i])
                    break
            for i in range(len(self.operators)): #caso esteja no operador
                if self.operators[i].call != None:
                    if self.operators[i].call.id == commandId:
                        mes = self.operators[i].hangup()
                        output.append(mes)    
        #Delegação de tarefa para operador disponível                   
        if len(self.callsQ) > 0:
            i = self.findAvailable()
            if i != None:
                mes = self.operators[i].ring(self.callsQ[0], self)
                output.append(mes)
                self.callsQ=self.callsQ[1:]#retira da fila
        message = json.dumps({'line':output}).encode('utf-8')
        return message


class QOTDFactory(Factory):
    def buildProtocol(self, addr):
        return QOTD()

endpoint = TCP4ServerEndpoint(reactor, 5768)
endpoint.listen(QOTDFactory())
reactor.run()