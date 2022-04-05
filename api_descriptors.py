from enum import Enum
from queue import Queue

class EndPointMethodReplyType(Enum):
    Response = "Response"
    Event = "Event"
    ResponseAndEvent = "ResponseAndEvent"

class EndPointMethodType(Enum):
    Public = "Public"
    Private = "Private"

class RotatingQueue(Queue):
    def __init__(self, maxsize=0):
        super().__init__(maxsize=maxsize)

    def put(self, item, block=True, timeout=None):
        if self.full():
            del self.queue[0]
        super().put(item, block, timeout)

class EndPointMethodDescriptor(object):
    def __init__(self, 
        methodType = EndPointMethodType.Private, 
        methodReplyType = EndPointMethodReplyType.Response, 
        methodQueue = RotatingQueue(maxsize=100), associatedEvent = "None"):
        self.methodType = methodType
        self.methodReplyType = methodReplyType
        self.methodQueue = methodQueue
        self.associatedEvent = associatedEvent