from threading import Thread
from queue import Empty
from datetime import datetime
from time import sleep
import websocket
import websocket._logging as wsLogging
import json
from typing import Union, Any, List, Tuple
import hmac
import hashlib

from api_descriptors import EndPointMethodDescriptor, EndPointMethodReplyType, EndPointMethodType, RotatingQueue
from log_service import DefaultLogger, WebSocketLogger
from message_enums import MessageType
from message_frame import MessageFrame
from message_request import CancelReplaceOrderRequest, \
    OrderFeeRequest, SendOrderRequest

from helpers import formatTicks, formatL2Snapshots

MAX_QUEUE_SIZE = 100
ONE_SHOT_TIMEOUT = 5.0

class FoxBitClient(object):
    sequenceByMessageType = {
        MessageType.Request: 0,
        MessageType.Reply: 0,
        MessageType.Subscribe: 0,
        MessageType.Event: 0,
        MessageType.Unsubscribe: 0,
        MessageType.Error: 0,
    }
    endPointDescriptorByMethod = {
        # Private
        "GetAvailablePermissionList": EndPointMethodDescriptor(),
        "GetUserConfig": EndPointMethodDescriptor(),
        "GetUserInfo": EndPointMethodDescriptor(),
        "GetUserPermissions": EndPointMethodDescriptor(),
        "RemoveUserConfig": EndPointMethodDescriptor(),
        "SetUserConfig": EndPointMethodDescriptor(),
        "SetUserInfo": EndPointMethodDescriptor(),
        "CancelAllOrders": EndPointMethodDescriptor(),
        "CancelOrder": EndPointMethodDescriptor(),
        "CancelQuote": EndPointMethodDescriptor(),
        "CancelReplaceOrder": EndPointMethodDescriptor(),
        "GetAccountInfo": EndPointMethodDescriptor(),
        "GetAccountPositions": EndPointMethodDescriptor(),
        "GetAccountTrades": EndPointMethodDescriptor(),
        "GetAccountTransactions": EndPointMethodDescriptor(),
        "GetOpenOrders": EndPointMethodDescriptor(),
        "SendOrder": EndPointMethodDescriptor(),
        "GetOrderFee": EndPointMethodDescriptor(),
        "GetOrderHistory": EndPointMethodDescriptor(),
        "GetDepositTickets": EndPointMethodDescriptor(),
        "GetWithdrawTickets": EndPointMethodDescriptor(),
        "GetDepositTicket": EndPointMethodDescriptor(),
        "GetWithdrawTicket": EndPointMethodDescriptor(),
        # Public
        "WebAuthenticateUser": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public
        ),
        "AuthenticateUser": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public
        ),
        "Authenticate2FA": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public
        ),
        "LogOut": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "ResetPassword": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "GetAccountFees": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "GetInstrument": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "GetInstruments": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "GetProduct": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "GetProducts": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "GetL2Snapshot": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "GetTickerHistory": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "SubscribeLevel1": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.ResponseAndEvent,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
          associatedEvent="Level1UpdateEvent",
        ),
        "SubscribeLevel2": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.ResponseAndEvent,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
          associatedEvent="Level2UpdateEvent",
        ),
        "SubscribeTicker": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.ResponseAndEvent,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "UnsubscribeLevel1": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "UnsubscribeLevel2": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "UnsubscribeTicker": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "SubscribeTrades": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        ),
        "UnsubscribeTrades": EndPointMethodDescriptor(
          methodReplyType=EndPointMethodReplyType.Response,
          methodQueue=RotatingQueue(maxsize=MAX_QUEUE_SIZE),
          methodType=EndPointMethodType.Public,
        )
    }

    socket: websocket.WebSocket
    logger: DefaultLogger
    connectionLogger: WebSocketLogger

    def __init__(self, enableConnLog=True):
        # Only alias for SubscribeLevel1
        self.endPointDescriptorByMethod["Level1UpdateEvent"] = self.endPointDescriptorByMethod["SubscribeLevel1"]
        # Only alias for SubscribeLevel2
        self.endPointDescriptorByMethod["Level2UpdateEvent"] = self.endPointDescriptorByMethod["SubscribeLevel2"]
        # Only alias for SubscribeTicker
        self.endPointDescriptorByMethod["TickerDataUpdateEvent"] = self.endPointDescriptorByMethod["SubscribeTicker"]
        # Only alias for SubscribeTrade
        self.endPointDescriptorByMethod["TradeDataUpdateEvent"] = self.endPointDescriptorByMethod["SubscribeTrades"]
        self.enableConnLog = enableConnLog
        self.logger = DefaultLogger()
        self.connectionLogger = WebSocketLogger()
        self.connectQueue = RotatingQueue(maxsize=MAX_QUEUE_SIZE)
        self.thread = None
        self.userId = None
        self.sessionToken = None

    def is_error_message(self, message_payload: dict) -> bool:
      return ("errorcode" in message_payload and "result" in message_payload and message_payload["errorcode"])

    '''
    * Connect to FoxBit websocket endpoint
    *
    * @param {string} [url='wss://api.foxbit.com.br']
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def connect(self, url: str = "wss://api.foxbit.com.br") -> bool:
        if self.enableConnLog:
          websocket.enableTrace(True, handler=self.connectionLogger.handlers[-1])
          wsLogging._logger = self.connectionLogger
        connected = True
        try:
            self.socket = websocket.WebSocketApp(
                url,
                on_open=self.onOpen,
                on_message=self.onMessage,
                on_close=self.onClose,
                on_error=self.onError
            )
            self.thread = Thread(target=self.socket.run_forever, args=(None, None, 30, 25), daemon=True)
            self.thread.start()
            while not self.isConnected():
              sleep(1)
        except Exception as e:
            connected = False
            print("Not possible to establish connection with {:s}".format(url))
            self.logger.warning("Not possible to establish connection with {:s}".format(url))

        return connected

    '''
    * Discover if websocket connection is open
    *
    * @readonly
    * @type {boolean}
    * @memberof FoxBitClient
    '''
    def isConnected(self) -> bool:
        return self.socket and self.socket.sock is not None and self.socket.sock.connected

    '''
    * Disconnect from FoxBit websocket connection
    *
    * @memberof FoxBitClient
    '''
    def disconnect(self):
        if self.isConnected():
            self.socket.close(status=websocket.STATUS_NORMAL)
            self.thread.join()

    # Open event handler
    def onOpen(self, socket):
        #print("Connection established.")
        self.logger.info("Connection established.")

    # Close event handler
    def onClose(self, socket, status_code, close_message):
        if status_code is not None and status_code > 1000:
          #print("Connection terminated. Status code {:d}: {:s}".format(status_code, close_message))
          self.logger.info("Connection terminated. Status code {:d}: {:s}".format(status_code, close_message))
        else:
          #print("Connection terminated normally.")
          self.logger.info("Connection terminated normally.")

        if status_code is not None and status_code != 0:
          for prop in self.endPointDescriptorByMethod.keys():
            endPointDescriptorByMethod = self.endPointDescriptorByMethod[prop]
            endPointDescriptorByMethod.methodQueue.put(close_message)

    # Error event handler
    def onError(self, socket, error):
      print("Socket error: {}".format(error))
      self.logger.error("Socket error: {}".format(error))
      self.connectQueue.put(error)

      for prop in self.endPointDescriptorByMethod.keys():
        endPointDescriptorByMethod = self.endPointDescriptorByMethod[prop]
        endPointDescriptorByMethod.methodQueue.put(error)

    def onMessage(self, socket, message):
      self.logger.debug("Message received (raw): {}".format(message))

      response_json = json.loads(message)
      response = MessageFrame(
        messageType=response_json['m'], 
        functionName=response_json['n'], 
        payload=response_json['o'], 
        sequence=response_json['i'])
      if response.payload:
        response.payload = json.loads(response.payload)
      self.logger.debug("Message received (parsed): {}".format(response.payload))

      endPointDescriptorByMethod = self.endPointDescriptorByMethod[response.functionName]

      if self.is_error_message(response.payload):
        # GenericResponse
        err = response.payload
        print("Error {}: {} {}".format(err["errorcode"], err["errormsg"], err["detail"]))
        self.logger.error("Error {}: {} {}".format(err["errorcode"], err["errormsg"], err["detail"]))
        endPointDescriptorByMethod.methodQueue.put(err)
      else:
        endPointDescriptorByMethod.methodQueue.put(response.payload)
        
      return

    def calculateMessageFrameSequence(self, messageFrame: MessageFrame):
      if messageFrame.messageType == MessageType.Request or \
        messageFrame.messageType == MessageType.Subscribe or \
        messageFrame.messageType == MessageType.Unsubscribe:
        self.sequenceByMessageType[messageFrame.messageType] += 2
        messageFrame.sequence = self.sequenceByMessageType[messageFrame.messageType]
      else:
        self.sequenceByMessageType[messageFrame.messageType] += 1
        messageFrame.sequence = self.sequenceByMessageType[messageFrame.messageType]

    def prepareAndSendFrame(self, frame: MessageFrame):
      self.calculateMessageFrameSequence(frame)
      frameStr = frame.to_json()

      self.logger.debug("Message sent: {}".format(frameStr))
      # Reset RotatingQueue
      with self.endPointDescriptorByMethod[frame.functionName].methodQueue.mutex:
        self.endPointDescriptorByMethod[frame.functionName].methodQueue.queue.clear()
      # Send message
      self.socket.send(frameStr)
      return

    def getResponse(self, endPointName: str) -> Any:
      response = None
      try:
        response = self.endPointDescriptorByMethod[endPointName].methodQueue.get(block=True, timeout=ONE_SHOT_TIMEOUT)
      except Empty:
        print("Method \'{:s}\' timed out.".format(endPointName))

      return response

    '''
    * Logout ends the current websocket session
    * **********************
    * Endpoint Type: Public
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def logOut(self) -> bool:
      endPointName = "LogOut"
      frame = MessageFrame(MessageType.Request, endPointName, {})
      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      loggedOut = False
      if response is not None and not self.is_error_message(response):
        loggedOut = response["result"]
        if loggedOut:
          self.disconnect()
      
      return loggedOut

    '''
    * WebAuthenticateUser authenticates a user (logs in a user) for the current websocket session.
    * You must call WebAuthenticateUser in order to use the calls in this document not otherwise shown as
    * "No authentication required."
    * **********************
    * Endpoint Type: Public
    * @param {string} username The name of the user, for example, jsmith.
    * @param {string} password The user password. The user logs into a specific Order Management
    * System via Secure Socket Layer (SSL and HTTPS).
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def webAuthenticateUser(self, username: str, password: str) -> bool:
      endPointName = "WebAuthenticateUser"
      frame = MessageFrame(
          MessageType.Request, endPointName, 
          {
            "Username": username,
            "Password": password
          })

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      authenticated = False
      if response is not None and not self.is_error_message(response):
        authenticated = response["Authenticated"]
        if authenticated:
          if "UserId" in response:
            self.userId = response["UserId"]
          if "SessionToken" in response:
            self.sessionToken = response["SessionToken"]
      
      return authenticated

    '''
    * Completes the second part of a two-factor authentication by sending the authentication token from
    * the non-AlphaPoint authentication system to the Order Management System. The call returns a
    * verification that the user logging in has been authenticated, and a token.
    * Here is how the two-factor authentication process works:
    *   1. Call WebAuthenticateUser. The response includes values for TwoFAType and
    *      TwoFAToken. For example, TwoFAType may return “Google,” and the TwoFAToken then
    *      returns a Google-appropriate token (which in this case would be a QR code).
    *   2. Enter the TwoFAToken into the two-factor authentication program, for example, Google
    *      Authenticator. The authentication program returns a different token.
    *   3. Call Authenticate2FA with the token you received from the two-factor authentication
    *      program (shown as YourCode in the request example below).
    *
    * @param {string} code Code holds the token obtained from the other authentication source.
    * @param {string} [sessionToken] To send a session token to re-establish an interrupted session
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def authenticate2FA(self, code: str) -> bool:
      endPointName = "Authenticate2FA"
      frame = MessageFrame(MessageType.Request, endPointName, {"Code": code})
      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      authenticated = False
      if response is not None and not self.is_error_message(response):
        authenticated = response["Authenticated"]
        if authenticated:
          if "UserId" in response:
            self.userId = response["UserId"]
          if "SessionToken" in response:
            self.sessionToken = response["SessionToken"]

      return authenticated

    '''
    * AuthenticateUser authenticates a user (logs in a user) for the current websocket session.
    * You must call WebAuthenticateUser in order to use the calls in this document not otherwise shown as
    * "No authentication required."
    * **********************
    * Endpoint Type: Public
    * @param {number} userId The ID of the user, for example, 1.
    * @param {string} apiKey user key for the FoxBit API
    * @param {string} apiSecret user secret for the FoxBit API 
    * System via Secure Socket Layer (SSL and HTTPS).
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def authenticateUser(self, apiKey: str, apiSecret: str, userId: int) -> bool:
      endPointName = "AuthenticateUser"
      nonce = int(round(datetime.utcnow().timestamp() * 1e3))
      signature_args = "{:d}{:d}{:s}".format(nonce, userId, apiKey)
      signature = hmac.new(
        bytes(apiSecret , 'utf-8'), 
        msg = bytes(signature_args , 'utf-8'), 
        digestmod = hashlib.sha256).hexdigest()
      param = {
        "APIKey": apiKey,
        "UserId": userId,
        "Signature": signature,
        "Nonce": nonce
      }
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      authenticated = False
      if response is not None and not self.is_error_message(response):
        authenticated = response["Authenticated"]
        if authenticated:
          if "UserId" in response:
            self.userId = response["UserId"]
          if "SessionToken" in response:
            self.sessionToken = response["SessionToken"]
      
      return authenticated

    '''
    * ResetPassword is a two-step process. The first step calls ResetPassword with the user’s username.
    * The Order Management System then sends an email to the user’s registered email address. The
    * email contains a reset link. Clicking the link sends the user to a web page where he can enter a new
    * password.
    * **********************
    * Endpoint Type: Public
    * @param {string} username The name of the user, for example, jsmith.
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def resetPassword(self, username: str) -> bool:
      endPointName = "ResetPassword"
      frame = MessageFrame(MessageType.Request, endPointName, {"UserName": username})

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      resetTriggered = False
      if response is not None and not self.is_error_message(response):
        resetTriggered = response["result"]

      return resetTriggered

    '''
    * Retrieves Fee structure for specific Account
    * **********************
    * Endpoint Type: Public
    * @param {number} accountId The ID of the account for which information was requested.
    * @param {number} omsId The ID of the Order Management System that includes the product.
    * @returns {List, Dict}
    * @memberof FoxBitClient
    '''
    def getAccountFees(self, accountId: int, omsId: int) -> Union[List[dict], dict]:
      endPointName = "GetAccountFees"
      frame = MessageFrame(MessageType.Request, endPointName, 
        {
          "AccountId": accountId,
          "OMSId": omsId,
        })

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      fees = None
      if response is not None and not self.is_error_message(response):
        fees = response

      return fees

    '''
    * Retrieves the details about a specific product on the trading venue. A product is an asset that is
    * tradable or paid out.
    * **********************
    * Endpoint Type: Public
    * @param {number} omsId The ID of the Order Management System that includes the product
    * @param {number} productId The ID of the product (often a currency) on the specified
    * Order Management System.
    * @returns {Dict}
    * @memberof FoxBitClient
    '''
    def getProduct(self, omsId: int, productId: int) -> dict:
      endPointName = "GetProduct"
      frame = MessageFrame(MessageType.Request, endPointName, 
        {
          "OMSId": omsId,
          "ProductId": productId
        })

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      product = None
      if response is not None and not self.is_error_message(response):
        product = response

      return product

    '''
    * Retrieves the details of a specific instrument from the Order Management System of the trading
    * venue. An instrument is a pair of exchanged products (or fractions of them) such as US dollars and
    * ounces of gold.
    * **********************
    * Endpoint Type: Public
    * @param {number} omsId The ID of the Order Management System from where the instrument is traded.
    * @param {number} instrumentId The ID of the instrument.
    * @returns {Dict}
    * @memberof FoxBitClient
    '''
    def getInstrument(self, omsId: int, instrumentId: int) -> dict:
      endPointName = "GetInstrument"
      frame = MessageFrame(MessageType.Request, endPointName, 
      {
        "OMSId": omsId,
        "InstrumentId": instrumentId,
      })

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      instrument = None
      if response is not None and not self.is_error_message(response):
        instrument = response

      return instrument
    '''
    * Retrieves the details of a specific instrument from the Order Management System of the trading
    * venue. An instrument is a pair of exchanged products (or fractions of them) such as US dollars and
    * ounces of gold.
    * **********************
    * Endpoint Type: Public
    * @param {number} omsId The ID of the Order Management System on which the instruments are available.
    * @returns {List[Dict]}
    * @memberof FoxBitClient
    '''
    def getInstruments(self, omsId: int) -> List[dict]:
      endPointName = "GetInstruments"
      frame = MessageFrame(MessageType.Request, endPointName, {"OMSId": omsId})

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      instruments = None
      if response is not None and not self.is_error_message(response):
        instruments = response

      return instruments

    '''
    * Returns an array of products available on the trading venue. A product is an asset that is tradable
    * or paid out
    * **********************
    * Endpoint Type: Public
    * @param {number} omsId The ID of the Order Management System that includes the product
    * @returns {List[Dict]}
    * @memberof FoxBitClient
    '''
    def getProducts(self, omsId: int) -> List[dict]:
      endPointName = "GetProducts"
      frame = MessageFrame(MessageType.Request, endPointName, {"OMSId": omsId})

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      products = None
      if response is not None and not self.is_error_message(response):
        products = response

      return products

    '''
    * Provides a current Level 2 snapshot of a specific instrument trading on an Order Management
    * System to a user-determined market depth
    * **********************
    * Endpoint Type: Public
    * @param {number} omsId The ID of the Order Management System where the instrument is traded.
    * @param {number} instrumentId The ID of the instrument that is the subject of the snapshot.
    * @param {number} [depth=100] in this call is "depth of market," the number of buyers and sellers at greater or lesser prices in
    * the order book for the instrument.
    * @returns {List[Dict]}
    * @memberof FoxBitClient
    '''
    def getL2Snapshot(self, omsId: int, instrumentId: int, depth: int = 100) -> List[dict]:
      endPointName = "GetL2Snapshot"
      frame = MessageFrame(MessageType.Request, endPointName, {
        "OMSId": omsId,
        "InstrumentId": instrumentId,
        "Depth": depth
      })

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      snapshotsResponse = None
      if response is not None and not self.is_error_message(response):
        snapshotsResponse = formatL2Snapshots(response)

      return snapshotsResponse

    '''
    * Requests a ticker history (high, low, open, close, volume, bid, ask, ID) of a specific instrument
    * from a given date forward to the present. You will need to format the returned data per your
    * requirements.
    * **********************
    * Endpoint Type: Public
    * @param {number} omsId The ID of the Order Management System.
    * @param {number} instrumentId The ID of a specific instrument. The Order Management System
    * and the default Account ID of the logged-in user are assumed.
    * @param {Date} fromDate Oldest date from which the ticker history will start, in 'yyyy-MM-ddThh:mm:ssZ' format.
    * The report moves toward the present from this point.
    * @param {Date} [toDate=Date()]
    * @param {number} [interval=60] Interval in minutes to consider tickers
    * @returns {List[Dict]}
    * @memberof FoxBitClient
    '''
    def getTickerHistory(self,
      omsId: int,
      instrumentId: int,
      fromDate: datetime,
      toDate: datetime = datetime.utcnow().replace(minute=0, second=0, microsecond=0),
      interval: int = 300) -> List[dict]:
      endPointName = "GetTickerHistory"
      frame = MessageFrame(MessageType.Request, endPointName, 
        {
          "OMSId": omsId,
          "InstrumentId": instrumentId,
          "Interval": interval,
          "FromDate": fromDate.strftime("%Y-%m-%dT%H:%M:%S"), # POSIX-format date and time
          "ToDate": toDate.strftime("%Y-%m-%dT%H:%M:%S"),
        })

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      ticks = None
      if response is not None and not self.is_error_message(response):
        ticks = formatTicks(response)

      return ticks

    '''
    * Retrieves the latest Level 1 Ticker information and then subscribes the user to ongoing Level 1
    * market data event updates for one specific instrument. For more information about Level 1
    * and Level 2. The SubscribeLevel1 call responds with the Level 1 response shown below.
    * The OMS then periodically sends *Leve1UpdateEvent* information when best bid/best offer
    * issues in the same format as this response, until you send the UnsubscribeLevel1 call.
    * **********************
    * Endpoint Type: Public
    * @param {number} omsId The ID of the Order Management System on which the instrument trades.
    * @param {(number | string)} instrumentIdOrSymbol The ID of the instrument you’re tracking.
    * or The symbol of the instrument you’re tracking.
    * @returns {RotatingQueue} (where the events will be pushed)
    * @memberof FoxBitClient
    '''
    def subscribeLevel1(self, omsId: int, instrumentIdOrSymbol: Union[int, str]) -> RotatingQueue: 
      param = dict()
      if isinstance(instrumentIdOrSymbol, int):
        param["OMSId"] = omsId
        param["InstrumentId"] = instrumentIdOrSymbol
      else:
        param["OMSId"] = omsId
        param["Symbol"] = instrumentIdOrSymbol

      frame = MessageFrame(MessageType.Request, "SubscribeLevel1", param)

      self.prepareAndSendFrame(frame)

      return self.endPointDescriptorByMethod["SubscribeLevel1"].methodQueue

    '''
    * Retrieves the latest Level 2 Ticker information and then subscribes the user to Level 2 market data
    * event updates for one specific instrument. Level 2 allows the user to specify the level of market
    * depth information on either side of the bid and ask. The SubscribeLevel2 call responds
    * with the Level 2 response shown below. The OMS then periodically sends *Level2UpdateEvent*
    * information in the same format as this response until you send the UnsubscribeLevel2 call.
    * **********************
    * Endpoint Type: Public
    * @param {number} omsId The ID of the Order Management System on which the instrument trades.
    * @param {(number | string)} instrumentIdOrSymbol The ID of the instrument you’re tracking
    * or The symbol of the instrument you’re tracking
    * @param {number} depth Depth in this call is “depth of market”, the number of buyers and sellers at greater or lesser prices in
    * the order book for the instrument.
    * @returns {RotatingQueue}
    * @memberof FoxBitClient
    '''
    def subscribeLevel2(self, omsId: int, instrumentIdOrSymbol: Union[int, str], depth: int = 300) -> RotatingQueue:
      param = dict()
      if isinstance(instrumentIdOrSymbol, int):
        param["OMSId"] = omsId
        param["InstrumentId"] = instrumentIdOrSymbol
        param["Depth"] = depth
      else:
        param["OMSId"] = omsId
        param["Symbol"] = instrumentIdOrSymbol
        param["Depth"] = depth

      frame = MessageFrame(MessageType.Request, "SubscribeLevel2", param)

      self.prepareAndSendFrame(frame)

      return self.endPointDescriptorByMethod["SubscribeLevel2"].methodQueue

    '''
    * Subscribes a user to a Ticker Market Data Feed for a specific instrument and interval.
    * SubscribeTicker sends a response object as described below, and then periodically returns a
    * *TickerDataUpdateEvent* that matches the content of the response object.
    * **********************
    * Endpoint Type: Public
    * @param {number} omsId The ID of the Order Management System
    * @param {number} instrumentId The ID of the instrument whose information you want to track.
    * @param {number} [interval=60]  Specifies in seconds how frequently to obtain ticker updates.
    * Default is 60 — one minute.
    * @param {number} [includeLastCount=100] The limit of records returned in the ticker history. The default is 100.
    * @returns {RotatingQueue}
    * @memberof FoxBitClient
    '''
    def subscribeTicker(self, 
      omsId: int,
      instrumentId: int,
      interval: int = 60,
      includeLastCount: int = 100) -> RotatingQueue:
      param = {
        "OMSId": omsId,
        "InstrumentId": instrumentId,
        "Interval": interval,
        "IncludeLastCount": includeLastCount,
      }
      frame = MessageFrame(MessageType.Request, "SubscribeTicker", param)

      self.prepareAndSendFrame(frame)

      return self.endPointDescriptorByMethod["SubscribeTicker"].methodQueue

    '''
    * Unsubscribes the user from a Level 1 Market Data Feed subscription..
    * **********************
    * Endpoint Type: Public
    * @param {number} omsId  The ID of the Order Management System on which the user has
    * subscribed to a Level 1 market data feed.
    * @param {number} instrumentId The ID of the instrument being tracked by the Level 1 market data feed.
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def unsubscribeLevel1(self, omsId: int, instrumentId: int) -> bool:
      endPointName = "UnsubscribeLevel1"
      param = {"OMSId": omsId, "InstrumentId": instrumentId}
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      unsubscribed = False
      if response is not None and not self.is_error_message(response):
        unsubscribed = response["result"]

      return unsubscribed

    '''
    * Unsubscribes the user from a Level 2 Market Data Feed subscription.
    * **********************
    * Endpoint Type: Public
    * @param {number} omsId  The ID of the Order Management System on which the user has
    * subscribed to a Level 2 market data feed.
    * @param {number} instrumentId The ID of the instrument being tracked by the Level 2 market data feed.
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def unsubscribeLevel2(self, omsId: int, instrumentId: int) -> bool:
      endPointName = "UnsubscribeLevel2"
      param = {"OMSId": omsId, "InstrumentId": instrumentId}
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      unsubscribed = False
      if response is not None and not self.is_error_message(response):
        unsubscribed = response["result"]

      return unsubscribed

    '''
    * Unsubscribes a user from a Ticker Market Data Feed
    * **********************
    * Endpoint Type: Public
    * @param {number} omsId  The ID of the Order Management System on which the user has
    * subscribed to a ticker market data feed.
    * @param {number} instrumentId The ID of the instrument being tracked by the ticker market data feed.
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def unsubscribeTicker(self, omsId: int, instrumentId: int) -> bool:
      endPointName = "UnsubscribeTicker"
      param = {"OMSId": omsId, "InstrumentId": instrumentId}
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      unsubscribed = False
      if response is not None and not self.is_error_message(response):
        unsubscribed = response["result"]

      return unsubscribed

    '''
    * Retrieves the latest public market trades and Subscribes User to Trade updates for the
    * specified Instrument.
    * ******************
    * **When subscribed to Trades, you will receive TradeDataUpdateEvent messages from the server**
    * @param {number} omsId Order Management System ID
    * @param {number} instrumentId Instrument's Identifier
    * @param {number} [includeLastCount=100] Specifies the number of previous trades to
    * retrieve in the immediate snapshot. Default is 100.
    * @returns {RotatingQueue}
    * @memberof FoxBitClient
    '''
    def subscribeTrades(self, omsId: int, instrumentId: int, includeLastCount: int = 100) -> RotatingQueue:
      endPointName = "SubscribeTrades"
      param = {
        "OMSId": omsId,
        "InstrumentId": instrumentId,
        "IncludeLastCount": includeLastCount,
      }

      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      return self.endPointDescriptorByMethod[endPointName].methodQueue

    '''
    * Unsubscribes a user from the Trades Market Data Feed.
    * @param {number} omsId The ID of the Order Management System on which the user has
    * subscribed to a trades market data feed.
    * @param {number} instrumentId The ID of the instrument being tracked by the trades
    * market data feed.
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def unsubscribeTrades(self, omsId: int, instrumentId: int) -> bool:
      endPointName = "UnsubscribeTrades"
      param = {"OMSId": omsId, "InstrumentId": instrumentId}

      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      unsubscribed = False
      if response is not None and not self.is_error_message(response):
        unsubscribed = response["result"]

      return unsubscribed

    # ============== Private Endpoints ================
    '''
    * **************************
    * API returns 'Endpoint not found'
    * **************************
    * Retrieves a comma-separated array of all permissions that can be assigned to a user.
    * An administrator or superuser can set permissions for each user on an API-call by API-call
    * basis, to allow for highly granular control. Common permission sets include Trading, Deposit,
    * and Withdrawal (which allow trading, deposit of funds, and account withdrawals, respectively)
    * or AdminUI, UserOperator, and AccountOperator (which allow control of the Order Management
    * System, set of users, or an account).
    * **********************
    * Endpoint Type: Private
    * @returns {List[String]}
    * @memberof FoxBitClient
    '''
    def getAvailablePermissionList(self) -> List[str]:
      endPointName = "GetAvailablePermissionList"
      param = {}
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      permissionList = None
      if response is not None and not self.is_error_message(response):
        permissionList = response

      return permissionList

    '''
    * **GetUserConfig** returns the list of key/value pairs set by the **SetUserConfig** call and associated with
    * a user record. A trading venue can use Config strings to store custom information or compliance
    * information with a user record.
    *
    * @returns {List[Dict]}
    * @memberof FoxBitClient
    '''
    def getUserConfig(self) -> List[dict]:
      endPointName = "GetUserConfig"
      param = {}
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      userConfig = None
      if response is not None and not self.is_error_message(response):
        userConfig = response

      return userConfig

    '''
    * Retrieves basic information about a user from the Order Management System. A user may only see
    * information about himself an administrator (or superuser) may see, enter, or change information
    * about other users
    *
    * @returns {Dict}
    * @memberof FoxBitClient
    '''
    def getUserInfo(self) -> dict:
      endPointName = "GetUserInfo"
      param = {}
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      userInfo = None
      if response is not None and not self.is_error_message(response):
        userInfo = response

      return userInfo

    '''
    * Retrieves an array of permissions for the logged-in user. Permissions can be set only by an
    * administrator or superuser.
    * An administrator or superuser can set permissions for each user on an API-call by API-call
    * basis, to allow for highly granular control. Common permission sets include Trading, Deposit,
    * and Withdrawal (which allow trading, deposit of funds, and account withdrawals, respectively)
    * or AdminUI, UserOperator, and AccountOperator (which allow control of the Order Management
    * System, set of users, or an account)
    *
    * @param {number} userId  The ID of the user whose permission information will be returned. A user
    * can only retrieve his own permissions an administrator can retrieve information
    * about the permissions of others.
    * @returns {List[String]}
    * @memberof FoxBitClient
    '''
    def getUserPermissions(self, userId: int) -> List[str]:
      endPointName = 'GetUserPermissions'
      param = {"UserId": userId}

      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      userPermissions = None
      if response is not None and not self.is_error_message(response):
        userPermissions = response

      return userPermissions

    '''
    * RemoveUserConfig deletes a single key/value Config pair from a user record. A trading venue uses
    * onfig strings to store custom information or compliance information with a user’s record.
    *
    * @param {number} userId The ID of the user from whose record you’re deleting the custom key/value pair
    * @param {string} userName The name of the user from whose record you’re deleting the custom key/value pair
    * @param {string} key The name of the key/value pair to delete
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def removeUserConfig(self, userId: int, userName: str, key: str) -> bool:
      endPointName = 'RemoveUserConfig'
      param = {
        "UserId": userId,
        "UserName": userName,
        "Key": key,
      }

      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      configRemoved = False
      if response is not None and not self.is_error_message(response):
        configRemoved = response["result"]

      return configRemoved

    '''
    * SetUserConfig adds an array of one or more arbitrary key/value pairs to a user record. A trading
    * venue can use Config strings to store custom information or compliance information with a user’s record.
    *
    * @param {number} userId The ID of the user to whose record you’re adding the custom key/value pairs.
    * @param {string} userName The name of the user to whose record you’re adding the custom key/value pairs.
    * @param {{}} config array of key/value pairs. “Key” is always a string but the associated Value of Key
    * can be of any data type.
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def setUserConfig(self, userId: int, userName: str, config: List[dict]) -> bool:
      endPointName = "SetUserConfig"
      param = {
        "UserId": userId,
        "UserName": userName,
        "Config": config,
      }

      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      configSet = False
      if response is not None and not self.is_error_message(response):
        configSet = response["result"]

      return configSet

    '''
    * Enters basic information about a user into the Order Management System. A user may only
    * enter or change information about himself an administrator (or superuser) may enter or change
    * information about other users.
    *
    * @param {number} userId The ID of the user set by the system when the user registers.
    * @param {string} userName User’s name “John Smith.”
    * @param {string} password User’s password.
    * @param {string} email User’s email address.
    * @param {boolean} emailVerified  Send true if you have verified the user’s email send false if you have
    * not verified the email address. Default is false.
    * @param {number} accountId The ID of the default account with which the user is associated. A user
    * may be associated with more than one account, and more than one user may be
    * associated with a single account. An admin or superuser can specify additional accounts
    * @param {boolean} use2FA  Set to true if this user must use two-factor authentication set to false if
    * this user does not need to user two-factor authentication. Default is false.
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def setUserInfo(self, 
      userId: int,
      userName: str,
      password: str,
      email: str,
      emailVerified: bool,
      accountId: int,
      use2FA: bool) -> bool:

      endPointName = "SetUserInfo"
      param = {
        "UserId": userId,
        "UserName": userName,
        "Password": password,
        "Email": email,
        "EmailVerified": emailVerified,
        "AccountId": accountId,
        "Use2FA": use2FA,
      }

      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      userInfoSet = False
      if response is not None and not self.is_error_message(response):
        userInfoSet = response["result"]

      return userInfoSet

    '''
    * Cancels all open matching orders for the specified instrument, account, user (subject to permission level)
    * or a combination of them on a specific Order Management System.
    * User and account permissions govern cancellation actions.
    *
    * | UserId 37 | AccId 14 | Instr 25 |                                    Result                                   |
    * |:---------:|:--------:|:--------:|:---------------------------------------------------------------------------:|
    * |     X     |     X    |     X    | Account #14 belonging to user #37 for instrument #25.                       |
    * |     X     |     X    |          | Account #14 belonging to user #37 for all instruments.                      |
    * |     X     |          |     X    | All accounts belonging to user #37 for instrument #25.                      |
    * |     X     |          |          | All accounts belonging to user #37 for all instruments.                     |
    * |           |     X    |     X    | All users of account #14 for instrument #25.                                |
    * |           |     X    |          | All users of account #14 for all instruments.                               |
    * |           |          |     X    | All accounts of all users for instrument #25. (requires special permission) |
    * |           |          |          | All accounts of all users for all instruments (requires special permission) |
    *
    * @param {number} omsId The Order Management System under which the account operates.Required
    * @param {number} [accountId] The account for which all orders are being canceled. Conditionally optional.
    * @param {number} [userId] The ID of the user whose orders are being canceled. Conditionally optional.
    * @param {number} [instrumentId] The ID of the instrument for which all orders are being cancelled. Conditionally optional.
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def cancelAllOrders(self, 
      omsId: int, 
      accountId: int = None, 
      userId: int = None, 
      instrumentId: int = None) -> bool:
      
      endPointName = "CancelAllOrders"
      param = {"OMSId": omsId}
      if accountId is not None:
        param["AccountId"] = accountId
      if userId is not None:
        param["UserId"] = userId
      if instrumentId is not None:
        param["InstrumentId"] = instrumentId
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      ordersCancelled = False
      if response is not None and not self.is_error_message(response):
        ordersCancelled = response["result"]

      return ordersCancelled

    '''
    * Cancels an open order that has been placed but has not yet been executed. Only a trading venue
    * operator can cancel orders for another user or account
    *
    * @param {number} omsId The Order Management System on which the order exists. Required
    * @param {number} [accountId]  The ID of account under which the order was placed. Conditionally optional.
    * @param {number} [clientOrderId] A user-assigned ID for the order (like a purchase-order number
    * assigned by a company). ClientOrderId defaults to 0. Conditionally optional.
    * @param {number} [orderId] The order to be cancelled. Conditionally optional
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def cancelOrder(self,
      omsId: int,
      accountId: int = None,
      orderId: int = None,
      clientOrderId: int = None) -> bool:
      
      endPointName = "CancelOrder"
      param = {
        "OMSId": omsId,
        "AccountId": accountId if accountId is not None else '',
        "OrderId": orderId if orderId is not None else ''
      }
      if clientOrderId is not None:
        param['ClientOrderId'] = clientOrderId

      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      orderCancelled = False
      if response is not None and not self.is_error_message(response):
        orderCancelled = response["result"]

      return orderCancelled

    '''
    * Cancels a quote that has not been executed yet.
    * Quoting is not enabled for the retail end user of the AlphaPoint software.
    * Only registered market participants or market makers may quote.
    * Only a trading venue operator can cancel quotes for another user.
    *
    * @param {number} omsId The ID of the Order Management System where the quote was requested. Required
    * @param {number} bidQuoteId The ID of the bid quote. Required.
    * @param {number} askQuoteId The ID of the ask quote. Required
    * @param {number} [accountId] The ID of the account that requested the quote. Conditionally optional
    * @param {number} [instrumentId] The ID of the instrument being quoted. Conditionally optional.
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def cancelQuote(self,
      omsId: int,
      bidQuoteId: int,
      askQuoteId: int,
      accountId: int = None,
      instrumentId: int = None) -> bool:
      endPointName = "CancelQuote"
      param = {
        "OMSId": omsId,
        "BidQuoteId": bidQuoteId,
        "AskQuoteId": askQuoteId,
        "AccountId": accountId if accountId is not None else '',
        "InstrumentId": instrumentId if instrumentId is not None else ''
      }

      frame = MessageFrame(MessageType.Request, endPointName, param)
      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      quoteCancelled = False
      if response is not None and not self.is_error_message(response):
        quoteCancelled = response["result"]

      return quoteCancelled

    '''
    * CancelReplaceOrder is single API call that both cancels an existing order and replaces it with a
    * order. Canceling one order and replacing it with another also cancels the order’s priority in
    * the order book. You can use ModifyOrder to preserve priority in the book but ModifyOrder only
    * allows a reduction in order quantity.
    * `Note: ` CancelReplaceOrder sacrifices the order’s priority in the order book.
    * @param {CancelReplaceOrderRequest} cancelReplaceOrderReq
    * @returns {boolean}
    * @memberof FoxBitClient
    '''
    def cancelReplaceOrder(self, cancelReplaceOrderReq: CancelReplaceOrderRequest) -> bool:
      endPointName = "CancelReplaceOrder"
      frame = MessageFrame(MessageType.Request, endPointName, cancelReplaceOrderReq)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      orderCancelled = True
      if response is not None and not self.is_error_message(response):
        orderCancelled = response["result"]

      return orderCancelled

    '''
    * Returns detailed information about one specific account belonging to the authenticated user and
    * existing on a specific Order Management System
    *
    * @param {number} omsId The ID of the Order Management System on which the account exists
    * @param {number} accountId  The ID of the account on the Order Management System for which information will be returned.
    * @param {string} accountHandle  AccountHandle is a unique user-assigned name that is checked at create
    * time by the Order Management System. Alternate to Account ID.
    * @returns {Dict}
    * @memberof FoxBitClient
    '''
    def getAccountInfo(self, omsId: int, accountId: int, accountHandle: str = "") -> dict:
      endPointName = "GetAccountInfo"
      param = {
        "OMSId": omsId,
        "AccountId": accountId,
        "AccountHandle": accountHandle,
      }

      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      accountInfo = None
      if response is not None and not self.is_error_message(response):
        accountInfo = response

      return accountInfo

    '''
    * Retrieves a list of positions (balances) for a specific user account running
    * under a specific Order Management System.
    * The trading day runs from UTC Midnight to UTC Midnight.
    * @param {number} accountId  The ID of the authenticated user’s account on the Order Management
    * System for which positions will be returned.
    * @param {number} omsId  The ID of the Order Management System to which the user belongs.
    * A user will belong only to one OMS.
    * @returns {List[Dict]}
    * @memberof FoxBitClient
    '''
    def getAccountPositions(self, accountId: int, omsId: int) -> List[dict]:
      endPointName = "GetAccountPositions"
      param = {"OMSId": omsId, "AccountId": accountId}
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      accountPositions = None
      if response is not None and not self.is_error_message(response):
        accountPositions = response

      return accountPositions

    '''
    * Requests the details on up to `200` past trade executions for a single specific user account and its
    * Order Management System, starting at index `i`, where `i` is an integer identifying a specific execution
    * in reverse order that is, the most recent execution has an index of `0`, and increments by one as trade
    * executions recede into the past.
    * The operator of the trading venue determines how long to retain an accessible trading history
    * before archiving.
    * @param {number} accountId The ID of the authenticated user’s account.
    * @param {number} omsId The ID of the Order Management System to which the user belongs.
    * A user will belong only to one OMS.
    * @param {number} startIndex The starting index into the history of trades, from `0`
    * (the most recent trade).
    * @param {number} count The number of trades to return. The system can return up to `200` trades.
    * @returns {List[Dict]}
    * @memberof FoxBitClient
    '''
    def getAccountTrades(self, 
      accountId: int,
      omsId: int,
      startIndex: int,
      count: int) -> List[dict]:
      
      endPointName = "GetAccountTrades"
      param = {
        "OMSId": omsId,
        "AccountId": accountId,
        "StartIndex": startIndex,
        "Count": count,
      }
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      accountTrades = None
      if response is not None and not self.is_error_message(response):
        accountTrades = response

      return accountTrades

    '''
    * Returns a list of transactions for a specific account on an Order Management System.
    * The owner of the trading venue determines how long to retain order history before archiving.
    * @param {number} accountId The ID of the account for which transactions will be returned.
    * If not specified, the call returns transactions for the default account for the logged-in user
    * @param {number} omsId The ID of the Order Management System from which the account’s
    * transactions will be returned.
    * @param {number} depth The number of transactions that will be returned, starting with
    * the most recent transaction.
    * @returns {List[Dict]}
    * @memberof FoxBitClient
    '''
    def getAccountTransactions(self, accountId: int, omsId: int, depth: int) -> List[dict]:
      endPointName = "GetAccountTransactions"
      param = {
        "OMSId": omsId,
        "AccountId": accountId,
        "Depth": depth,
      }
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      accountTransactions = None
      if response is not None and not self.is_error_message(response):
        accountTransactions = response

      return accountTransactions

    '''
    * Returns an array of 0 or more orders that have not yet been filled (open orders) for a single account
    * for a given user on a specific Order Management System. The call returns an empty array if a user
    * has no open orders.
    * @param {number} accountId The ID of the authenticated user’s account
    * @param {number} omsId The ID of the Order Management System to which the user belongs.
    * A user will belong only to one OMS.
    * @returns {List[Dict]}
    * @memberof FoxBitClient
    '''
    def getOpenOrders(self, accountId: int, omsId: int) -> List[dict]:
      endPointName = "GetOpenOrders"
      param = {"OMSId": omsId, "AccountId": accountId}
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      openOrders = None
      if response is not None and not self.is_error_message(response):
        openOrders = response

      return openOrders

    '''
    * Creates an order. Anyone submitting an order should also subscribe to the various market data and
    * event feeds, or call GetOpenOrders or GetOrderStatus to monitor the status of the order. If the
    * order is not in a state to be executed, GetOpenOrders will not return it.
    * @param {SendOrderRequest} sendOrderRequest
    * @returns {Tuple[boolean, number]}
    * @memberof FoxBitClient
    '''
    def sendOrder(self, sendOrderRequest: SendOrderRequest) -> Tuple[bool, int]:
      endPointName = "SendOrder"

      frame = MessageFrame(MessageType.Request, endPointName, sendOrderRequest)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      orderProcessed = False
      orderId = -1
      if response is not None and not self.is_error_message(response):
        orderProcessed = response["status"] == "Accepted"
        orderId = response["OrderId"]

      return orderProcessed, orderId

    '''
    * Returns an estimate of the fee for a specific order and order type.
    * Fees are set and calculated by the operator of the trading venue.
    * @param {OrderFeeRequest} orderFeeRequest
    * @returns {Dict}
    * @memberof FoxBitClient
    '''
    def getOrderFee(self, orderFeeRequest: OrderFeeRequest) -> dict:
      endPointName = "GetOrderFee"
      frame = MessageFrame(MessageType.Request, endPointName, orderFeeRequest)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      orderFeeInfo = None
      if response is not None and not self.is_error_message(response):
        orderFeeInfo = response

      return orderFeeInfo

    '''
    * Returns a complete list of all orders, both open and executed, for a specific account on the specified
    * Order Management System.
    * @param {number} accountId The ID of the Order Management System where the orders were placed
    * @param {number} omsId The ID of the account whose orders will be returned
    * @returns {List[Dict]}
    * @memberof FoxBitClient
    '''
    def getOrderHistory(self, accountId: int, omsId: int) -> List[dict]:
      endPointName = "GetOrderHistory"
      param = {"OMSId": omsId, "AccountId": accountId}
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      orderHistory = None
      if response is not None and not self.is_error_message(response):
        orderHistory = response

      return orderHistory

    '''
    * Returns all deposit tickets in the database.
    * ************
    * Only admin-level users can issue this call.
    * @param {number} omsId  The ID of the Order Management System where the withdrawal was made.
    * @param {number} operatorId  The ID of the trading venue operator on the system where
    * the deposit was made.
    * @param {number} accountId The ID of the account from which the withdrawal was made.
    * @returns {List[Dict]}
    * @memberof FoxBitClient
    '''
    def getDepositTickets(self, omsId: int, operatorId: int, accountId: int) -> List[dict]:
      endPointName = "GetDepositTickets"
      param = {
        "OMSId": omsId,
        "OperatorId": operatorId,
        "AccountId": accountId,
      }
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      depositTickets = None
      if response is not None and not self.is_error_message(response):
        depositTickets = response

      return depositTickets

    '''
    * Returns all withdraw tickets in the database.
    * ************
    * Only admin-level users can issue this call.
    * @param {number} omsId  The ID of the Order Management System where the withdrawal was made.
    * @param {number} operatorId  The ID of the trading venue operator on the system where
    * the withdraw was made.
    * @param {number} accountId The ID of the account from which the withdrawal was made.
    * @returns {List[Dict]}
    * @memberof FoxBitClient
    '''
    def getWithdrawTickets(self, omsId: int, operatorId: int, accountId: int) -> List[dict]:
      endPointName = "GetWithdrawTickets"
      param = {
        "OMSId": omsId,
        "OperatorId": operatorId,
        "AccountId": accountId,
      }
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      withdrawTickets = None
      if response is not None and not self.is_error_message(response):
        withdrawTickets = response

      return withdrawTickets

    '''
    * Returns a single deposit ticket by matching its request code to one already in the database.
    * ************
    * Only admin-level users can issue this call.
    * @param {number} omsId  The ID of the Order Management System where the deposit was made.
    * @param {number} operatorId  The ID of the trading venue operator on the system where
    * the withdraw was made.
    * @param {string} requestCode A GUID (globally unique ID) that identifies the specific withdrawal ticket
    * you want to return. Obtain the RequestCode from **GetDepositTickets**.
    * @param {number} accountId The ID of the account from which the deposit was made.
    * @returns {Dict}
    * @memberof FoxBitClient
    '''
    def getDepositTicket(self, 
      omsId: int,
      operatorId: int,
      requestCode: str,
      accountId: int) -> dict:
      endPointName = "GetDepositTicket"
      param = {
        "OMSId": omsId,
        "OperatorId": operatorId,
        "RequestCode": requestCode,
        "AccountId": accountId,
      }

      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      depositTicket = None
      if response is not None and not self.is_error_message(response):
        depositTicket = response

      return depositTicket

    '''
    * Returns a single withdraw ticket from the Order Management System, trading venue operator, and
    * account that matches the GUID (globally unique identifier) in RequestCode. Obtain the GUID from
    * the call CreateWithdrawTicket when the ticket is first created, or from GetAllWithdrawTickets,
    * another admin-level-only call. An administrator can use GetWithdrawTicket to return any single
    * withdrawal ticket in the system.
    * @param {number} omsId  The ID of the Order Management System where the withdrawal was made.
    * @param {number} operatorId  The ID of the trading venue operator on the system where
    * the withdraw was made.
    * @param {string} requestCode A GUID (globally unique ID) that identifies the specific withdrawal ticket
    * you want to return. Obtain the RequestCode from **GetWithdrawTickets**.
    * @param {number} accountId The ID of the account from which the withdrawal was made.
    * @returns {Dict}
    * @memberof FoxBitClient
    '''
    def getWithdrawTicket(self,
      omsId: int,
      operatorId: int,
      requestCode: str,
      accountId: int) -> dict:
      endPointName = "GetWithdrawTicket"
      param = {
        "OMSId": omsId,
        "OperatorId": operatorId,
        "RequestCode": requestCode,
        "AccountId": accountId,
      }
      frame = MessageFrame(MessageType.Request, endPointName, param)

      self.prepareAndSendFrame(frame)

      response = self.getResponse(endPointName)
      withdrawTicket = None
      if response is not None and not self.is_error_message(response):
        withdrawTicket = response

      return withdrawTicket