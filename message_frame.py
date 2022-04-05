from helpers import jsonStringify

class MessageFrame(object):
    def __init__(self, messageType, functionName, payload = None, sequence = 0):
        self.messageType = messageType
        self.functionName = functionName
        self.sequence = 0
        self.payload = payload

    def to_json(self):
        return jsonStringify(
            {
                'm': self.messageType.value, 
                'i': self.sequence, 
                'n': self.functionName, 
                'o': self.payload
            })