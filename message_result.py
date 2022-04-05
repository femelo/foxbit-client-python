from message_enums import ActionType, ChangeReasonResponse, DepositStatusResponse, FeeCalcTypeResponse
from message_enums import InstrumentType, MarketPriceDirection, OrderStateResponse, OrderType, OrderTypeResponse
from dataclasses import dataclass
from message_enums import ProductType, SendOrderStatusResponse, SessionStatus, Side, SideResponse, WithdrawStatus
from typing import Any, List
from numbers import Number
from datetime import datetime

@dataclass
class GenericResponse:
    '''
    If the call has been successfully received by the Order Management System,
    result is true; otherwise, it is false.
    @type {boolean}
    @memberof GenericResponse
    '''
    result: bool

    '''
    A successful receipt of the call returns null; the errormsg parameter for an unsuccessful call returns one of the following messages:
    - Not Authorized (errorcode 20)
    - Invalid Request (errorcode 100)
    - Operation Failed (errorcode 101)
    - Server Error (errorcode 102)
    - Resource Not Found (errorcode 104)
    @type {string}
    @memberof GenericResponse
    '''
    errormsg: str

    '''
    A successful receipt of the call returns 0.
    An unsuccessful receipt of the call returns one of the errorcodes
    shown in the errormsg list.
    - Not Authorized (errorcode 20)
    - Invalid Request (errorcode 100)
    - Operation Failed (errorcode 101)
    - Server Error (errorcode 102)
    - Resource Not Found (errorcode 104)
    @type {number}
    @memberof GenericResponse
    '''
    errorcode: Number

    '''
    Message text that the system may send.
    The content of this parameter is usually null.
    @type {string}
    @memberof GenericResponse
    '''
    detail: str


@dataclass
class AccountFeesResponse:
    '''
    Unique identifier for a fee
    @type {number}
    @memberof AccountFeesResponse
    '''
    FeeId: Number

    '''
    Fee amount
    @type {number}
    @memberof AccountFeesResponse
    '''
    FeeAmt: Number

    FeeCalcType: FeeCalcTypeResponse

    FeeType: str

    LadderThreshold: Number

    LadderSeconds: Number

    IsActive: bool

    InstrumentId: Number

    OrderType: str

    OMSId: Number

    AccountId: Number


@dataclass
class AuthenticateResponse:
    Authenticated: bool

    SessionToken: str

    UserId: Number

    twoFaToken: str


@dataclass
class InstrumentResponse:
    OMSId: Number

    InstrumentId: Number

    Symbol: str

    Product1: Number

    Product1Symbol: str

    Product2: Number

    Product2Symbol: str

    InstrumentType: InstrumentType

    VenueInstrumentId: Number

    VenueId: Number

    SortIndex: Number

    SessionStatus: SessionStatus

    PreviousSessionStatus: SessionStatus

    SessionStatusDateTime: datetime

    SelfTradePrevention: bool

    QuantityIncrement: Number


@dataclass
class ProductResponse:
    OMSId: Number

    ProductId: Number

    Product: str

    ProductFullName: str

    ProductType: ProductType

    DecimalPlaces: Number

    TickSize: Number

    NoFees: bool


@dataclass
class L2SnapshotResponse:
    MDUpdateID: Number

    Accounts: Number

    ActionDateTime: Number

    ActionType: ActionType

    LastTradePrice: Number

    Orders: Number

    Price: Number

    ProductPairCode: Number

    Quantity: Number

    Side: Side


@dataclass
class SubscriptionLevel1Response:
    OMSId: Number

    InstrumentId: Number

    BestBid: Number

    BestOffer: Number

    LastTradedPx: Number

    LastTradedQty: Number

    LastTradeTime: Number

    SessionOpen: Number

    SessionHigh: Number

    SessionLow: Number

    SessionClose: Number

    Volume: Number

    CurrentDayVolume: Number

    CurrentDayNumTrades: Number

    CurrentDayPxChange: Number

    Rolling24HrVolume: Number

    Rolling24NumTrades: Number

    Rolling24HrPxChange: Number

    TimeStamp: Number


@dataclass
class SubscriptionL2Response:
    MDUpdateID: Number

    Accounts: Number

    ActionDateTime: Number

    ActionType: ActionType

    LastTradePrice: Number

    Orders: Number

    Price: Number

    ProductPairCode: Number

    Quantity: Number

    Side: Side


@dataclass
class SubscriptionTickerResponse:
    TickerDate: Number

    High: Number

    Low: Number

    Open: Number

    Close: Number

    Volume: Number

    BidPrice: Number

    AskPrice: Number

    InstrumentId: Number


@dataclass
class SubscriptionTradesResponse:
    TradeId: Number

    InstrumentId: Number

    Quantity: Number

    Price: Number

    Order1: Number

    Order2: Number

    Tradetime: Number

    Direction: MarketPriceDirection

    TakerSide: Side

    BlockTrade: bool

    Order1or2ClientId: Number


@dataclass
class UserInfoResponse:
    '''
    ID number of the user whose information is being set.
    
    @type {number}
    @memberof UserInfoResponse
    '''
    UserId: Number

    '''
    Log-in name of the user; “jsmith”
    
    @type {string}
    @memberof UserInfoResponse
    '''
    UserName: str

    '''
    Email address of the user; “person@company.com”.
    
    @type {string}
    @memberof UserInfoResponse
    '''
    Email: str

    '''
    Not currently used. Returns an empty string.
    
    @type {string}
    @memberof UserInfoResponse
    '''
    PasswordHash: str

    '''
    Usually contains an empty string. Contains a GUID — a globally unique ID string — during the time that
    a new user has been sent a registration email and before the user clicks the confirmation link.
    @type {string}
    @memberof UserInfoResponse
    '''
    PendingEmailCode: str

    '''
    Has your organization verified this email as correct and operational? True if yes; false if no.
    Defaults to false.
    
    @type {boolean}
    @memberof UserInfoResponse
    '''
    EmailVerified: bool

    '''
    The ID of the default account with which the user is associated.
    
    @type {number}
    @memberof UserInfoResponse
    '''
    AccountId: Number

    '''
    The date and time at which this user record was created, in ISO 8601 format.
    
    @type {number}
    @memberof UserInfoResponse
    '''
    DateTimeCreated: Number

    '''
    The ID of an affiliated organization, if the user comes from an affiliated link.
    This is set to 0 if the user it not associated with an affiliated organization.
    
    @type {number}
    @memberof UserInfoResponse
    '''
    AffiliatedId: Number

    '''
    Captures the ID of the person who referred this account member to the trading venue,
    usually for marketing purposes.
    Returns 0 if no referrer.
    
    @type {number}
    @memberof UserInfoResponse
    '''
    RefererId: Number

    '''
    The ID of the Order Management System with which the user is associated.
    
    @type {number}
    @memberof UserInfoResponse
    '''
    OMSId: Number

    '''
    True if the user must use two-factor authentication;
    false if the user does not need to use two-factor authentication. Defaults to false.
    
    @type {boolean}
    @memberof UserInfoResponse
    '''
    Use2FA: bool

    '''
    Reserved for future use. Currently returns an empty string
    
    @type {string}
    @memberof UserInfoResponse
    '''
    Salt: str

    '''
    A date and time in ISO 8601 format. Reserved.
    
    @type {number}
    @memberof UserInfoResponse
    '''
    PendingCodeTime: Number


@dataclass
class CancelReplaceOrderResult:
    '''
    The order ID assigned to the replacement order by the server.
    
    @type {number}
    @memberof CancelReplaceOrderResult
    '''
    ReplacementOrderId: Number

    '''
    Echoes the contents of the ClientOrderId value from the request
    
    @type {number}
    @memberof CancelReplaceOrderResult
    '''
    ReplacementClOrdId: Number

    '''
    Echoes OrderIdToReplace, which is the original order you are replacing.
    
    @type {number}
    @memberof CancelReplaceOrderResult
    '''
    OrigOrderId: Number

    '''
    Provides the client order ID of the original order (not specified in the requesting call)
    
    @type {number}
    @memberof CancelReplaceOrderResult
    '''
    OrigClOrdId: Number


@dataclass
class AccountInfoResult:
    '''
    The ID of the Order Management System on which the account resides.
    @type {number}
    @memberof AccountInfoResult
    '''
    OMSID: Number

    '''
    The ID of the account for which information was requested.
    @type {number}
    @memberof AccountInfoResult
    '''
    AccountId: Number

    '''
    A non-unique name for the account assigned by the user
    @type {string}
    @memberof AccountInfoResult
    '''
    AccountName: str

    '''
    AccountHandle is a unique user-assigned name that is checked at create
    time by the Order Management System to assure its uniqueness.
    @type {string}
    @memberof AccountInfoResult
    '''
    AccountHandle: str

    '''
    An arbitrary identifier assigned by a trading venue operator to a trading
    firm as part of the initial company, user, and account set up process. For
    example, Smith Financial Partners might have the ID SMFP.
    @type {string}
    @memberof AccountInfoResult
    '''
    FirmId: str

    '''
    A longer, non-unique version of the trading firm’s name;
    for example, Smith Financial Partners.
    @type {string}
    @memberof AccountInfoResult
    '''
    FirmName: str

    '''
    The type of the account for which information is being returned. One of:
    - Asset
    - Liability
    - ProfitLoss
    
    Responses for this stringvalue pair for Market Participants are almost exclusively
    Asset.
    @type {Acc}
    @memberof AccountInfoResult
    '''
    AccountType: str

    '''
    Defines account attributes relating to how fees are calculated and
    assessed. Set by trading venue operator.
    @type {number}
    @memberof AccountInfoResult
    '''
    FeeGroupID: Number

    '''
    Reserved for future development.
    @type {number}
    @memberof AccountInfoResult
    '''
    ParentID: Number

    '''
    One of:
    - Unkown (an error condition)
    - Normal
    - NoRiskCheck
    - NoTrading
    
    Returns Normal for virtually all market participants. Other types indicate account
    configurations assignable by the trading venue operator.
    @type {string}
    @memberof AccountInfoResult
    '''
    RiskType: str

    '''
    Verification level ID (how much verification does this account require)
    defined by and set by the trading venue operator for this account.
    @type {number}
    @memberof AccountInfoResult
    '''
    VerificationLevel: Number

    '''
    One of:
    - BaseProduct
    - SingleProduct
    
    Trading fees may be charged by a trading venue operator. This value shows
    whether fees for this account’s trades are charged in the product being traded
    (BaseProduct, for example BitCoin) or whether the account has a preferred
    fee-paying product (SingleProduct, for example USD) to use in all cases and
    regardless of product being traded.
    @type {AccountTypeOrRiskTypeOrFeeProductType}
    @memberof AccountInfoResult
    '''
    FeeProductType: str

    '''
    The ID of the preferred fee product, if any. Defaults to 0
    @type {number}
    @memberof AccountInfoResult
    '''
    FeeProduct: Number

    '''
    Captures the ID of the person who referred this account to the trading
    venue, usually for marketing purposes.
    @type {number}
    @memberof AccountInfoResult
    '''
    RefererId: Number

    '''
    Comma-separated array. Reserved for future expansion.
    @type {number[]}
    @memberof AccountInfoResult
    '''
    SupportedVenueIds: List[Number]


@dataclass
class AccountPositionResult:
    '''
    The ID of the Order Management System (OMS) to which the user
    belongs. A user will only ever belong to one Order Management System.
    @type {number}
    @memberof AccountPositionResult
    '''
    OMSId: Number

    '''
    Returns the ID of the user’s account to which the positions belong.
    @type {number}
    @memberof AccountPositionResult
    '''
    AccountId: Number

    '''
    The symbol of the product on this account’s side of the trade. For
    example:
    - BTC — BitCoin
    - USD — US Dollar
    - NZD — New Zealand Dollar
    Many other values are possible depending on the nature of the trading venue.
    @type {string}
    @memberof AccountPositionResult
    '''
    ProductSymbol: str

    '''
    The ID of the product being traded. The system assigns product IDs as
    they are entered into the system
    Use GetProduct to return information about the product by its ID.
    @type {number}
    @memberof AccountPositionResult
    '''
    ProductId: Number

    '''
    Unit amount of the product; for example, 10 or 138.5
    @type {number}
    @memberof AccountPositionResult
    '''
    Amount: Number

    '''
    Amount of currency held and not available for trade. A pending trade of 100
    units at $1 each will reduce the amount in the account available for trading by
    $100. Amounts on hold cannot be withdrawn while a trade is pending.
    @type {number}
    @memberof AccountPositionResult
    '''
    Hold: Number

    '''
    Deposits accepted but not yet cleared for trade
    @type {number}
    @memberof AccountPositionResult
    '''
    PendingDeposits: Number

    '''
    Withdrawals acknowledged but not yet cleared from the account. Amounts
    in PendingWithdraws are not available for trade.
    @type {number}
    @memberof AccountPositionResult
    '''
    PendingWithdraws: Number

    '''
    Total deposits on today’s date. The trading day runs
    between UTC Midnight and UTC Midnight.
    @type {number}
    @memberof AccountPositionResult
    '''
    TotalDayDeposits: Number

    '''
    Total withdrawals on today’s date. The trading day runs
    between UTC Midnight and UTC Midnight.
    @type {number}
    @memberof AccountPositionResult
    '''
    TotalDayWithdraws: Number

    '''
    Total withdrawals during this month to date. The trading day runs between
    UTC Midnight and UTC Midnight — likewise a month begins at UTC Midnight on
    the first day of the month.
    @type {number}
    @memberof AccountPositionResult
    '''
    TotalMonthWithdraws: Number


@dataclass
class AccountTradesResult:
    '''
    The date and time stamp of the trade in Microsoft tick format and UTC time zone
    @type {number}
    @memberof AccountTradesResult
    '''
    TradeTimeMS: Number

    '''
    The fee for this trade in units and fractions of units (a $10 USD fee would be
    10.00, a .5-BitCoin fee would be 0.5).
    @type {number}
    @memberof AccountTradesResult
    '''
    Fee: Number

    '''
    The ID of the product that denominates the fee. Product types will vary
    on each trading venue. See GetProduct.
    @type {number}
    @memberof AccountTradesResult
    '''
    FeeProductId: Number

    '''
    The user ID of the user who entered the order that caused the trade for
    this account. (Multiple users can have access to an account.)
    @type {number}
    @memberof AccountTradesResult
    '''
    OrderOriginator: Number

    '''
    The ID of the Order Management System to which the user belongs.
    A user will belong only to one OMS.
    @type {number}
    @memberof AccountTradesResult
    '''
    OMSId: Number

    '''
    The ID of this account’s side of the trade. Every trade has two sides.
    @type {number}
    @memberof AccountTradesResult
    '''
    ExecutionId: Number

    '''
    The ID of the overall trade.
    @type {number}
    @memberof AccountTradesResult
    '''
    TradeId: Number

    '''
    The ID of the order causing the trade.
    @type {number}
    @memberof AccountTradesResult
    '''
    OrderId: Number

    '''
    The Account ID that made the trade.
    @type {number}
    @memberof AccountTradesResult
    '''
    AccountId: Number

    '''
    Not currently used.
    @type {number}
    @memberof AccountTradesResult
    '''
    SubAccountId: Number

    '''
    Your Client Order Id
    @type {number}
    @memberof AccountTradesResult
    '''
    ClientOrderId: Number

    '''
    The ID of the instrument being traded. See GetInstrument to find
    information about this instrument by its ID.
    @type {number}
    @memberof AccountTradesResult
    '''
    InstrumentId: Number

    '''
    Buy or Sell
    - 0 Buy
    - 1 Sell
    - 2 Short (reserved for future use)
    - 3 Unknown (error condition)
    @type {Side}
    @memberof AccountTradesResult
    '''
    Side: Side

    '''
    The unit quantity of the trade.
    @type {number}
    @memberof AccountTradesResult
    '''
    Quantity: Number

    '''
    The number of units remaining to be traded by the order after this
    execution. This number is not revealed to the other party in the trade. This value
    is also known as “leave size” or “leave quantity.”
    @type {number}
    @memberof AccountTradesResult
    '''
    RemainingQuantity: Number

    '''
    The unit price at which the instrument traded.
    @type {number}
    @memberof AccountTradesResult
    '''
    Price: Number

    '''
    The total value of the deal. The system calculates this as:
    unit price X quantity executed
    @type {number}
    @memberof AccountTradesResult
    '''
    Value: Number

    '''
    The time at which the trade took place, in POSIX format and UTC time zone
    @type {number}
    @memberof AccountTradesResult
    '''
    TradeTime: Number

    '''
    Shows 0
    @type {(number | null)}
    @memberof AccountTradesResult
    '''
    CounterParty: Number

    '''
    This value increments if the trade has changed. Default is 1.
    For example, if the trade busts (fails to conclude), the trade
    will need to be modified and a revision number then will apply.
    @type {number}
    @memberof AccountTradesResult
    '''
    OrderTradeRevision: Number

    '''
    Shows if this trade has moved the book price up, down, or no change.
    Values:
    - NoChange
    - UpTick
    - DownTick
    @type {string}
    @memberof AccountTradesResult
    '''
    Direction: MarketPriceDirection

    '''
    Returns true if the trade was a reported trade; false otherwise.
    @type {boolean}
    @memberof AccountTradesResult
    '''
    IsBlockTrade: bool


@dataclass
class OpenOrdersResult:
    '''
    The open order can be Buy or Sell.
    - 0 Buy
    - 1 Sell
    - 2 Short (reserved for future use)
    - 3 Unknown (error condition)
    @type {SideResponse}
    @memberof OpenOrdersResult
    '''
    Side: SideResponse

    '''
    The ID of the open order. The OrderID is unique in each Order Management Systsem.
    @type {number}
    @memberof OpenOrdersResult
    '''
    OrderId: Number

    '''
    The price at which the buy or sell has been ordered.
    @type {number}
    @memberof OpenOrdersResult
    '''
    Price: Number

    '''
    The quantity to be bought or sold.
    @type {number}
    @memberof OpenOrdersResult
    '''
    Quantity: Number

    '''
    The quantity available to buy or sell that is publicly displayed to the market.
    To display a DisplayQuantity value, an order must be a Limit order with a reserve.
    @type {number}
    @memberof OpenOrdersResult
    '''
    DisplayQuantity: Number

    '''
    ID of the instrument being traded. See GetInstruments
    @type {number}
    @memberof OpenOrdersResult
    '''
    Instrument: Number

    '''
    The ID of the account that placed the order
    @type {number}
    @memberof OpenOrdersResult
    '''
    Account: Number

    '''
    There are currently seven types of order
    @type {OrderType}
    @memberof OpenOrdersResult
    '''
    OrderType: OrderType

    '''
    A user-assigned ID for the order (like a purchase-order number assigned by a company).
    ClientOrderId defaults to 0.
    @type {number}
    @memberof OpenOrdersResult
    '''
    ClientOrderId: Number

    '''
    The current condition of the order. There are five order states:
    - Working
    - Rejected
    - Canceled
    - Expired
    - FullyExecuted
    @type {OrderStateResponse}
    @memberof OpenOrdersResult
    '''
    OrderState: OrderStateResponse

    '''
    The time at which the system received the order, in POSIX format and UTC time zone
    @type {number}
    @memberof OpenOrdersResult
    '''
    ReceiveTime: Number

    '''
    The time stamp of the received order in Microsoft Tick format, and UTC time zone
    @type {number}
    @memberof OpenOrdersResult
    '''
    ReceiveTimeTicks: Number

    '''
    Original quantity of the order. The quantity of the actual execution may
    be lower than this number, but OrigQuantity shows the quantity in the order as placed.
    @type {number}
    @memberof OpenOrdersResult
    '''
    OrigQuantity: Number

    '''
    The number of units executed in this trade.
    @type {number}
    @memberof OpenOrdersResult
    '''
    QuantityExecuted: Number

    '''
    Not currently used.
    @type {number}
    @memberof OpenOrdersResult
    '''
    AvgPrice: Number

    '''
    Shows 0.
    @type {number}
    @memberof OpenOrdersResult
    '''
    CounterPartyId: Number

    '''
    The reason that an order has been changed. Values:
    - 1 NewInputAccepted
    - 2 NewInputRejected
    - 3 OtherRejected
    - 4 Expired
    - 5 Trade
    - 6 SystemCanceled_NoMoreMarket
    - 7 SystemCanceled_BelowMinimum
    - 8 NoChange
    - 100 UserModified
    @type {ChangeReasonResponse}
    @memberof OpenOrdersResult
    '''
    ChangeReason: ChangeReasonResponse

    '''
    ID of the original order. This number is also appended to CancelReplaceOrder
    @type {number}
    @memberof OpenOrdersResult
    '''
    OrigOrderId: Number

    '''
    The Orignal Client-Designate Order Id.
    @type {number}
    @memberof OpenOrdersResult
    '''
    OrigClOrdId: Number

    '''
    User ID of the person who entered the order
    @type {number}
    @memberof OpenOrdersResult
    '''
    EnteredBy: Number

    '''
    True if the open order is a quote; false if not.
    @type {boolean}
    @memberof OpenOrdersResult
    '''
    IsQuote: bool

    '''
    Best price available at time of entry (for ask or bid, respectively).
    @type {number}
    @memberof OpenOrdersResult
    '''
    InsideAsk: Number

    '''
    Quantity available at the best inside ask (or bid) price.
    @type {number}
    @memberof OpenOrdersResult
    '''
    InsideAskSize: Number

    '''
    Best price available at time of entry (for ask or bid, respectively).
    @type {number}
    @memberof OpenOrdersResult
    '''
    InsideBid: Number

    '''
    Quantity available at the best inside ask (or bid) price.
    @type {number}
    @memberof OpenOrdersResult
    '''
    InsideBidSize: Number

    '''
    Last trade price for this product before this order was entered.
    @type {number}
    @memberof OpenOrdersResult
    '''
    LastTradePrice: Number

    '''
    If this order was rejected, RejectReason holds the reason for the rejection.
    @type {string}
    @memberof OpenOrdersResult
    '''
    RejectReason: str

    '''
    True if both parties to a block trade agree that one party will report
    the trade for both. Otherwise false.
    @type {boolean}
    @memberof OpenOrdersResult
    '''
    IsLockedIn: bool

    '''
    ID of the Order Management System on which the order was placed.
    @type {number}
    @memberof OpenOrdersResult
    '''
    OMSId: Number


@dataclass
class SendOrderResult:
    '''
    If the order is accepted by the system, it returns 0.
    - 0 Accepted
    - 1 Rejected
    @type {SendOrderStatusResponse}
    @memberof SendOrderResult
    '''
    status: SendOrderStatusResponse

    '''
    Any error message the server returns
    @type {string}
    @memberof SendOrderResult
    '''
    errormsg: str

    '''
    The ID assigned to the order by the server. This allows you to track the order.
    @type {number}
    @memberof SendOrderResult
    '''
    OrderId: Number


@dataclass
class OrderFeeResult:
    '''
    The estimated fee for the trade as described. The minimum value is 0.01.
    @type {number}
    @memberof OrderFeeResult
    '''
    OrderFee: Number

    '''
    The ID of the product (currency) in which the fee is denominated.
    @type {number}
    @memberof OrderFeeResult
    '''
    ProductId: Number


@dataclass
class OrderHistoryResult:
    '''
    The open order can be Buy or Sell.
    - 0 Buy
    - 1 Sell
    - 2 Short (reserved for future use)
    - 3 Unknown (error condition)
    @type {SideResponse}
    @memberof OrderHistoryResult
    '''
    Side: SideResponse

    '''
    The ID of this order
    @type {number}
    @memberof OrderHistoryResult
    '''
    OrderId: Number

    '''
    Price of the order.
    @type {number}
    @memberof OrderHistoryResult
    '''
    Price: Number

    '''
    Quantity of the order.
    @type {number}
    @memberof OrderHistoryResult
    '''
    Quantity: Number

    '''
    The quantity available to buy or sell that is publicly displayed to the market.
    To display a DisplayQuantity value, an order must be a Limit order with a reserve
    @type {number}
    @memberof OrderHistoryResult
    '''
    DisplayQuantity: Number

    '''
    The ID of the instrument being ordered.
    @type {number}
    @memberof OrderHistoryResult
    '''
    Instrument: Number

    '''
    The ID of the account ordering the instrument.
    @type {number}
    @memberof OrderHistoryResult
    '''
    Account: Number

    '''
    One of:
    - Unknown
    - Market
    - Limit
    - StopMarket
    - StopLimit
    - TrailingStopMarket
    - TrailingStopLimit
    - BlockTrade
    @type {OrderTypeResponse}
    @memberof OrderHistoryResult
    '''
    OrderType: OrderTypeResponse

    '''
    A user-assigned ID for the order (like a purchase-order number assigned by a company).
    ClientOrderId defaults to 0
    @type {number}
    @memberof OrderHistoryResult
    '''
    ClientOrderId: Number

    '''
    One of:
    - Unknown
    - Working
    - Rejected
    - Canceled
    - Expired
    - FullyExecuted
    An open order will probably not yet be fully executed.
    @type {OrderStateResponse}
    @memberof OrderHistoryResult
    '''
    OrderState: OrderStateResponse

    '''
    The time at which the system received the quote, in POSIX format
    @type {number}
    @memberof OrderHistoryResult
    '''
    ReceiveTime: Number

    '''
    The time stamp of the received quote in Microsoft Ticks format.
    @type {number}
    @memberof OrderHistoryResult
    '''
    ReceiveTimeTicks: Number

    '''
    If the order has been changed, this value shows the original quantity
    @type {number}
    @memberof OrderHistoryResult
    '''
    OrigQuantity: Number

    '''
    This value states the quantity that was executed in the order. It may be the
    same as the quantity of the order; it may be different.
    @type {number}
    @memberof OrderHistoryResult
    '''
    QuantityExecuted: Number

    '''
    Not currently used.
    @type {number}
    @memberof OrderHistoryResult
    '''
    AvgPrice: Number

    '''
    Shows 0
    @type {number}
    @memberof OrderHistoryResult
    '''
    CounterPartyId: Number

    '''
    The reason that an order has been changed. Values:
    - 1 NewInputAccepted
    - 2 NewInputRejected
    - 3 OtherRejected
    - 4 Expired
    - 5 Trade
    - 6 SystemCanceled_NoMoreMarket
    - 7 SystemCanceled_BelowMinimum
    - 8 NoChange
    - 100 UserModified
    @type {ChangeReasonResponse}
    @memberof OrderHistoryResult
    '''
    ChangeReason: ChangeReasonResponse

    '''
    If the order has been changed, shows the original order ID.
    @type {number}
    @memberof OrderHistoryResult
    '''
    OrigOrderId: Number

    '''
    If the order has been changed, shows the original client order ID, a
    value that the client can create (much like a purchase order).
    @type {number}
    @memberof OrderHistoryResult
    '''
    OrigClOrdId: Number

    '''
    The ID of the user who entered the order in this account.
    @type {number}
    @memberof OrderHistoryResult
    '''
    EnteredBy: Number

    '''
    If this order is a quote (rather than an order), returns true, otherwise false.
    Default is false.
    @type {boolean}
    @memberof OrderHistoryResult
    '''
    IsQuote: bool

    '''
    Best Ask price available at time of entry (generally available to market makers)
    @type {number}
    @memberof OrderHistoryResult
    '''
    InsideAsk: Number

    '''
    Quantity available at the best inside ask price (generally available to market makers).
    @type {number}
    @memberof OrderHistoryResult
    '''
    InsideAskSize: Number

    '''
    Best Bid price available at time of entry (generally available to market makers).
    @type {number}
    @memberof OrderHistoryResult
    '''
    InsideBid: Number

    '''
    Quantity available at the best inside Bid price (generally available to market makers).
    @type {number}
    @memberof OrderHistoryResult
    '''
    InsideBidSize: Number

    '''
    The price at which the instrument last traded.
    @type {number}
    @memberof OrderHistoryResult
    '''
    LastTradePrice: Number

    '''
    If the order was rejected, this string value holds the reason
    @type {string}
    @memberof OrderHistoryResult
    '''
    RejectReason: str

    '''
    True if both parties to a block trade agree that one party will report the
    trade for both. Otherwise false.
    @type {boolean}
    @memberof OrderHistoryResult
    '''
    IsLockedIn: bool

    '''
    The ID of the Order Management System on which the order was created.
    @type {number}
    @memberof OrderHistoryResult
    '''
    OMSId: Number


@dataclass
class AllDepositTicketsResult:
    '''
    The ID of the Asset Manager module, which interacts with the OMS and
    the trading venue’s matching engine. The Asset Manager accepts, holds, and
    disburses assets (products)
    @type {number}
    @memberof AllDepositTicketsResult
    '''
    AssetManagerId: Number

    '''
    The ID of the account into which the deposit was made.
    @type {number}
    @memberof AllDepositTicketsResult
    '''
    AccountId: Number

    '''
    The ID of the asset being deposited. Equivalent to product ID. AssetId = ProductId,
    and uses the same ID numbers.
    @type {number}
    @memberof AllDepositTicketsResult
    '''
    AssetId: Number

    '''
    The name of the asset being deposited. USD (dollars), BTC (bitcoin),
    gold, NZD (New Zealand dollars) for example. This is not an enumerated field, to
    allow for flexibility.
    @type {string}
    @memberof AllDepositTicketsResult
    '''
    AssetName: str

    '''
    The amount of the asset being deposited.
    @type {number}
    @memberof AllDepositTicketsResult
    '''
    Amount: Number

    '''
    The ID of the Order Management System handling the deposits.
    @type {number}
    @memberof AllDepositTicketsResult
    '''
    OMSId: Number

    '''
    A GUID (globally unique ID) string that identifies this specific deposit.
    @type {string}
    @memberof AllDepositTicketsResult
    '''
    RequestCode: str

    '''
    The on-line IP (Internet Protocol) address from which the deposit is made.
    This can be a traditional IPv4 dotted quad (192.168.168.1) or a 128-bit IPv6 address.
    @type {string}
    @memberof AllDepositTicketsResult
    '''
    RequestIP: str

    '''
    The ID of the user sending the request and making the deposit
    @type {number}
    @memberof AllDepositTicketsResult
    '''
    RequestUser: Number

    '''
    The name of the user sending the request and making the deposit.
    For example, “John Smith.”
    @type {string}
    @memberof AllDepositTicketsResult
    '''
    RequestUserName: str

    '''
    The ID of the operator of the trading venue
    @type {number}
    @memberof AllDepositTicketsResult
    '''
    OperatorId: Number

    '''
    The current status of the deposit. One of:
    - 0 New
    - 1 AdminProcessing
    - 2 Accepted
    - 3 Rejected
    - 4 SystemProcessing
    - 5 FullyProcessed
    - 6 Failed
    - 7 Pending
    
    Note: The value of Status is an integer in the request for GetAllDepositTickets.
    In the response, it is a string..
    
    @type {DepositStatusResponse}
    @memberof AllDepositTicketsResult
    '''
    Status: DepositStatusResponse

    '''
    The value of the fee for making the deposit, if any
    @type {number}
    @memberof AllDepositTicketsResult
    '''
    FeeAmt: Number

    '''
    The ID of the most recent user updating this deposit ticket
    @type {number}
    @memberof AllDepositTicketsResult
    '''
    UpdatedByUser: Number

    '''
    The name of the most recent user updating this deposit ticket,
    for example, “Joan Smith.”
    @type {string}
    @memberof AllDepositTicketsResult
    '''
    UpdatedByUserName: str

    '''
    A system-assigned unique deposit ticket number that identifies the
    deposit. The value for TicketNumber is returned by the GetDepositTicket calls:
    GetAllDepositTickets and GetDepositTicket
    @type {number}
    @memberof AllDepositTicketsResult
    '''
    TicketNumber: Number

    '''
    A list of strings and stringvalue pairs that holds information about the
    source of funds being deposited. This information was entered when the deposit
    ticket was created, and as required by the account provider.
    @type {string}
    @memberof AllDepositTicketsResult
    '''
    DepositInfo: str

    '''
    The time and date that the deposit was created, in ISO 8601 format.
    @type {string}
    @memberof AllDepositTicketsResult
    '''
    CreatedTimestamp: str

    '''
    The time and date that the deposit ticket last was updated, in ISO 8601 format.
    @type {string}
    @memberof AllDepositTicketsResult
    '''
    LastUpdateTimeStamp: str

    '''
    Comments are sets of system-generated stringvalue pairs
    that provide information about the deposit’s process through the system. Neither
    users nor admins enter these comments directly.
    @type {string[]}
    @memberof AllDepositTicketsResult
    '''
    Comments: List[str]

    '''
    A set of base-64 strings usually providing an image or a PDF.
    This image or file may be a transaction receipt or other information that the
    depositor wishes to attach to the deposit for record-keeping purposes.
    @type {string[]}
    @memberof AllDepositTicketsResult
    '''
    Attachments: List[str]


@dataclass
class AllWithdrawTicketsResult:
    '''
    The ID of the Asset Manager module.
    @type {number}
    @memberof AllWithdrawTicketsResult
    '''
    AssetManagerId: Number

    '''
    The ID of the account that made the withdrawal.
    @type {number}
    @memberof AllWithdrawTicketsResult
    '''
    AccountId: Number

    '''
    The ID of the asset in which the withdrawal is denominated, for example,
    US Dollar or BitCoin both have an associated AssetId. AssetId and ProductId are
    identical in numerical content. You must use AssetId here.
    @type {number}
    @memberof AllWithdrawTicketsResult
    '''
    AssetId: Number

    '''
    The readable name of the asset in which the withdrawal is denominated,
    for example, “US Dollar” or “BitCoin.”
    @type {string}
    @memberof AllWithdrawTicketsResult
    '''
    AssetName: str

    '''
    The amount of the withdrawal.
    @type {number}
    @memberof AllWithdrawTicketsResult
    '''
    Amount: Number

    '''
    See the TemplateForm object, following.
    The content of a template depends on the account provider that you use for
    deposits and withdrawals. This template is provided as a general reference example
    @type {}
    @memberof AllWithdrawTicketsResult
    '''
    TemplateForm: any

    '''
    The name of the template being used. The template controls the stringvalue
    pairs in the TemplateForm object returned for each withdrawal.
    These vary by account provider
    @type {string}
    @memberof AllWithdrawTicketsResult
    '''
    TemplateType: str

    '''
    The name of the template being used. The template controls the string
    value pairs in the TemplateForm object returned for each withdrawal. These vary
    by account provider
    @type {string}
    @memberof AllWithdrawTicketsResult
    '''
    TemplateFormType: str

    '''
    Any comment pertaining to the withdrawal
    @type {string}
    @memberof AllWithdrawTicketsResult
    '''
    Comment: str

    '''
    An external address supplied by the account provider to accept the withdrawal.
    @type {string}
    @memberof AllWithdrawTicketsResult
    '''
    ExternalAddress: str

    '''
    The ID of the Order Management System
    @type {number}
    @memberof AllWithdrawTicketsResult
    '''
    OMSId: Number

    '''
    A GUID (globally unique ID) string that identifies this specific withdrawal.
    @type {string}
    @memberof AllWithdrawTicketsResult
    '''
    RequestCode: str

    '''
    The IP address from which the withdrawal was initiated,
    in either IPv4 dotted quad format or IPv6 format.
    @type {string}
    @memberof AllWithdrawTicketsResult
    '''
    RequestIP: str

    '''
    The ID of the user who made the original withdrawal reques
    @type {number}
    @memberof AllWithdrawTicketsResult
    '''
    RequestUserId: Number

    '''
    The name of the user who made the original withdrawal request.
    @type {string}
    @memberof AllWithdrawTicketsResult
    '''
    RequestUserName: str

    '''
    The ID of the operator of the trading venue on which
    the withdrawal request was made.
    @type {number}
    @memberof AllWithdrawTicketsResult
    '''
    OperatorId: Number

    '''
    The current status of the deposit, stated as an integer. One of:
    - 0 New
    - 1 AdminProcessing
    - 2 Accepted
    - 3 Rejected
    - 4 SystemProcessing
    - 5 FullyProcessed
    - 6 Failed
    - 7 Pending
    - 8 Pending2Fa
    - 9 AutoAccepted
    - 10 Delayed
    
    Note: Withdraw tickets include Status values 8 through 10, which do
    not apply to deposit tickets. Status for GetAllWithdrawTickets and
    GetAllDepositTickets are numerical; other instances of Status are strings
    @type {WithdrawStatus}
    @memberof AllWithdrawTicketsResult
    '''
    Status: WithdrawStatus

    '''
    The amount of any fee that was charged for the withdrawal. FeeAmt is
    always denominated in the asset or product of the withdrawal, for example in US
    Dollars, BitCoin, or other currency, depending on the nature of the funds being
    withdrawn.
    @type {number}
    @memberof AllWithdrawTicketsResult
    '''
    FeeAmt: Number

    '''
    The ID of any user who made an update to the withdraw ticket.
    Updates are most usually to Status.
    @type {number}
    @memberof AllWithdrawTicketsResult
    '''
    UpdatedByUser: Number

    '''
    The name of any user who made an update to the withdraw ticket.
    Updates are most usually to Status
    @type {string}
    @memberof AllWithdrawTicketsResult
    '''
    UpdatedByUserName: str

    '''
    A system-assigned unique withdraw ticket number that identifies
    the withdrawal. The value for TicketNumber is returned by the Get~ calls:
    GetAllWithdrawTickets and GetWithdrawTicket.
    @type {number}
    @memberof AllWithdrawTicketsResult
    '''
    TicketNumber: Number

    '''
    The time and date at which the withdraw ticket was created,
    in ISO 8601 format.
    @type {string}
    @memberof AllWithdrawTicketsResult
    '''
    CreatedTimestamp: str

    '''
    If the ticket has been updated, shows the time and date stamp of the
    update in ISO 8601 format; if the ticket has not been updated, shows the same
    time and date stamp as CreateTimestamp
    @type {string}
    @memberof AllWithdrawTicketsResult
    '''
    LastUpdateTimestamp: str

    '''
    
    
    @type {Comment[]}
    @memberof AllWithdrawTicketsResult
    '''
    Comments: List[str]

    '''
    A set of base-64 strings usually providing an image or a PDF.
    This image or file may be a transaction receipt or other information that the
    depositor wishes to attach to the deposit for record-keeping purposes.
    @type {string[]}
    @memberof AllWithdrawTicketsResult
    '''
    Attachments: List[str]

    '''
    Reserved for future use.
    @type {any[]}
    @memberof AllWithdrawTicketsResult
    '''
    AuditLog: Any

