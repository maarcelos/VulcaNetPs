import cmd
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
import json

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



point = TCP4ClientEndpoint(reactor, "localhost", 5768)
protocol_instance = Greeter()
d = connectProtocol(point, protocol_instance)
reactor.callInThread(Commands(protocol_instance).cmdloop)
reactor.run()