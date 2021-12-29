#Classes
class Call:
    def __init__(self,id):
        self.id = id

class Operator:
    def __init__(self,id):
        self.id=id
        self.status = "AVAILABLE"
        self.call = None

#Functions
def findAvailable(operators):
    for i in range(len(operators)):
        if operators[i].status == "AVAILABLE":
            return i
    return None

def ring(call,availableOperator):
    print("Call {callId} ringing for operator {operatorId}".format(callId=call.id, operatorId=availableOperator.id))
    availableOperator.status = "RINGING"
    availableOperator.call = call
    return availableOperator

def answer(operator):
    print("Call {callId} answered by operator {operatorId}".format(callId=operator.call.id, operatorId=operator.id))
    operator.status = "BUSY"
    return operator

def reject(operator):
    rejecCall = operator.call
    print("Call {callId} rejected by operator {operatorId}".format(callId=operator.call.id, operatorId=operator.id))
    operator.status = "AVAILABLE"
    operator.call = None
    return operator,rejecCall

def hangup(operator):
    print("Call {callId} finished and operator {operatorId} available".format(callId=operator.call.id, operatorId=operator.id))
    operator.status = "AVAILABLE"
    operator.call = None
    return operator
#Variables inicialization
operators = []
operators.extend([Operator("A"),Operator("B")])

callsQ = []
inconsistence = 0

while(True):
    if len(callsQ) > 0:
        i = findAvailable(operators)
        if i != None:
            operators[i] = ring(callsQ[0],operators[i])
            callsQ=callsQ[1:]#retira da fila

 
 
    command, commandId = input().split()
    
    if command == "call":
        call = Call(commandId)
        callsQ.append(call)
        print("Call {callId} received".format(callId =commandId))
        if findAvailable(operators) == None:
            print("Call {callId} waiting in queue".format(callId=commandId))

    if command == "answer":
        for i in range(len(operators)):
            if operators[i].id == commandId:
                operators[i] = answer(operators[i])
    
    if command == "reject":
        for i in range(len(operators)):
            if operators[i].id == commandId:
                operators[i],rejectCall = reject(operators[i])
                callsQ.insert(0, rejectCall)
    if command == "hangup":
        #caso esteja na queue
        for i in range(len(callsQ)):
            if callsQ[i].id == commandId:
                print("Call {callId} missed".format(callId = callsQ[i].id))
                callsQ.remove(callsQ[i])
                break
        #caso esteja no operador
        for i in range(len(operators)):
            if operators[i].call != None:
                if operators[i].call.id == commandId:
                    if operators[i].status == "RINGING":
                        print("Call {callId} missed".format(callId =commandId))
                    if operators[i].status == "BUSY":
                        print("Call {callId} finished and operator {operatorId} available".format(callId = commandId, operatorId = operators[i].id))
                    operators[i].status = "AVAILABLE"
                    operators[i].call = None    
