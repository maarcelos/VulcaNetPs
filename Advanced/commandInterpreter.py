from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import stdio
from twisted.protocols import basic
import json
import cmd
from twisted.internet.protocol import Protocol
from twisted.internet import reactor


class Greeter(Protocol):
    def sendMessage(self, msg):
        self.transport.write(msg)
    def dataReceived(self,message):
        message = json.loads(message.decode('utf-8'))
        for m in message['line']:
            print(m)


class Commands(cmd.Cmd):
    prompt = ''
    def __init__(self, protocol):
        self.protocol = protocol
        super().__init__()

    def do_call(self,arg):
        message = json.dumps({"command":"call", "id":arg})
        self.protocol.sendMessage(message.encode('utf-8'))
    def do_answer(self,arg):
        message = json.dumps({"command":"answer", "id":arg})
        self.protocol.sendMessage(message.encode('utf-8'))
    def do_reject(self,arg):
        message = json.dumps({"command":"reject", "id":arg})
        self.protocol.sendMessage(message.encode('utf-8'))
    def do_hangup(self,arg):
        message = json.dumps({"command":"hangup", "id":arg})
        self.protocol.sendMessage(message.encode('utf-8'))



class Echo(basic.LineReceiver):
   from os import linesep as delimiter
   def __init__(self, console):
        self.console = console
        super().__init__() 

   def connectionMade(self):
        self.setRawMode()
    
   def rawDataReceived(self, data):
        self.console.onecmd(data.decode('utf-8'))
   

def main():
    point = TCP4ClientEndpoint(reactor, "localhost", 5678)
    protocol_instance = Greeter()
    d = connectProtocol(point, protocol_instance)
    stdio.StandardIO(Echo(Commands(protocol_instance)))
    reactor.run()

if __name__ == '__main__':
    main()