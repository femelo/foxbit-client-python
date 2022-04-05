from enum import Enum

class MessageType(Enum):
  Request = 0
  Reply = 1
  Subscribe = 2
  Event = 3
  Unsubscribe = 4
  Error = 5

class InstrumentType(Enum):
  Unknown = 0
  Standard = 1

class SessionStatus(Enum):
  Unknown = 0
  Running = 1
  Paused = 2
  Stopped = 3
  Starting = 4

class ProductType(Enum):
  Unknown = 0
  NationalCurrency = 1
  CryptoCurrency = 2
  Contract = 3

class Side(Enum):
  Buy = 0
  Sell = 1
  Short = 2
  Unknown = 3

class SideResponse(Enum):
  Buy = 0
  Sell = 1
  Short = 2
  Unknown = 3

class ActionType(Enum):
  New = 0
  Update = 1
  Delete = 2

class MarketPriceDirection(Enum):
  NoChange = 0
  UpTick = 1
  DownTick = 2

class PegPriceType(Enum):
  Unknown = 0
  Last = 1
  Bid = 2
  Ask = 3
  Midpoint = 4

class TimeInForce(Enum):
  Unknown = 0
  GTC = 1
  IOC = 2
  FOK = 3

class OrderType(Enum):
  Unknown = 0
  Market = 1
  Limit = 2
  StopMarket = 3
  StopLimit = 4
  TrailingStopMarket = 5
  TrailingStopLimit = 6
  BlockTrade = 7

class MakerTaker(Enum):
  Unknown = 'Unknown'
  Maker = 'Maker'
  Taker = 'Taker'

class OrderTypeResponse(Enum):
  Unknown = 'Unknown'
  Market = 'Market'
  Limit = 'Limit'
  StopMarket = 'StopMarket'
  StopLimit = 'StopLimit'
  TrailingStopMarket = 'TrailingStopMarket'
  TrailingStopLimit = 'TrailingStopLimit'
  BlockTrade = 'BlockTrade'

class OrderStateResponse(Enum):
  Working = 'Working'
  Rejected = 'Rejected'
  Canceled = 'Canceled'
  Expired = 'Expired'
  FullyExecuted = 'FullyExecuted'

class ChangeReasonResponse(Enum):
  NewInputAccepted = 'NewInputAccepted'
  NewInputRejected = 'NewInputRejected'
  OtherRejected = 'OtherRejected'
  Expired = 'Expired'
  Trade = 'Trade'
  SystemCanceled_NoMoreMarket = 'SystemCanceled_NoMoreMarket'
  SystemCanceled_BelowMinimum = 'SystemCanceled_BelowMinimum'
  NoChange = 'NoChange'
  UserModified = 'UserModified'

class SendOrderStatusResponse(Enum):
  Accepted = 'Accepted'
  Rejected = 'Rejected'

class DepositStatus(Enum):
  New = 0
  AdminProcessing = 1
  Accepted = 2
  Rejected = 3
  SystemProcessing = 4
  FullyProcessed = 5
  Failed = 6
  Pending = 7

class WithdrawStatus(Enum):
  New = 0
  AdminProcessing = 1
  Accepted = 2
  Rejected = 3
  SystemProcessing = 4
  FullyProcessed = 5
  Failed = 6
  Pending = 7
  Pending2Fa = 8
  AutoAccepted = 9
  Delayed = 10

class DepositStatusResponse(Enum):
  New = 'New'
  AdminProcessing = 'AdminProcessing'
  Accepted = 'Accepted'
  Rejected = 'Rejected'
  SystemProcessing = 'SystemProcessing'
  FullyProcessed = 'FullyProcessed'
  Failed = 'Failed'
  Pending = 'Pending'

class FeeCalcTypeResponse(Enum):
  Percentage = 'Percentage'
  FlatRate = 'FlatRate'

class AmountOperator(Enum):
  TicketsEqualToAmount = 0
  TicketsEqualOrGreaterThanAmount = 1
  TicketsLessThanAmount = 2
