from dataclasses import dataclass
from message_enums import AmountOperator, DepositStatus, MakerTaker, OrderType, PegPriceType, Side, TimeInForce
from numbers import Number

@dataclass
class CancelReplaceOrderRequest:
    '''
    The ID of the Order Management System on which the order is being canceled
    and replaced by another order.
    @type {number}
    @memberof CancelReplaceOrderRequest
    '''
    OMSId: Number

    '''
    The ID of the order to replace with this order.
    @type {number}
    @memberof CancelReplaceOrderRequest
    '''
    OrderIdToReplace: Number

    '''
    A user-assigned ID for the new, replacement order (like a
    purchase-order number assigned by a company). This ID is useful for recognizing
    future states related to this order. ClientOrderId defaults to 0.
    @type {number}
    @memberof CancelReplaceOrderRequest
    '''
    ClientOrdId: Number

    '''
    The type of the replacement order.
    - 0 Unknown
    - 1 Market
    - 2 Limit
    - 3 StopMarket
    - 4 StopLimit
    - 5 TrailingStopMarket
    - 6 TrailingStopLimit
    - 7 BlockTrade
    @type {OrderType}
    @memberof CancelReplaceOrderRequest
    '''
    OrderType: OrderType

    '''
    The side of the replacement order:
    - 0 Buy
    - 1 Sell
    - 2 Short (reserved for future use)
    - 3 Unknown (error condition)
    @type {Side}
    @memberof CancelReplaceOrderRequest
    '''
    Side: Side

    '''
    The ID of the account under which the original order was placed and the
    new order will be placed.
    @type {number}
    @memberof CancelReplaceOrderRequest
    '''
    AccountId: Number

    '''
    The ID of the instrument being traded.
    @type {number}
    @memberof CancelReplaceOrderRequest
    '''
    InstrumentId: Number

    '''
    The offset by which to trail the market in one of the trailing order types.
    Set this to the current price of the market to ensure that the trailing offset is the
    amount intended in a fast-moving market
    @type {number}
    @memberof CancelReplaceOrderRequest
    '''
    TrailingAmount: Number

    '''
    When entering a Trailing Limit order, set this to offset the activation price.
    This allows you to activate your order away from the market.
    @type {number}
    @memberof CancelReplaceOrderRequest
    '''
    LimitOffset: Number

    '''
    Quantity to Display on the Market. If your order is for 1000,
    and you only want to show 100 at a time in market data, set this to 100. Set to 0 to display all
    @type {number}
    @memberof CancelReplaceOrderRequest
    '''
    DisplayQuantity: Number

    '''
    The price at which to execute the new order, if the order is a Limit order.
    @type {number}
    @memberof CancelReplaceOrderRequest
    '''
    LimitPrice: Number

    '''
    The price at which to execute the new order, if the order is a Stop order
    (either buy or sell).
    @type {number}
    @memberof CancelReplaceOrderRequest
    '''
    StopPrice: Number

    '''
    When entering a stoptrailing order, set PegPriceType to the type of price
    that pegs the stop.
    - 1 Last
    - 2 Bid
    - 3 Ask
    - 4 Midpoint
    @type {PegPriceType}
    @memberof CancelReplaceOrderRequest
    '''
    PegPriceType: PegPriceType

    '''
    The period during which the new order is executable.
    - 0 Unknown (error condition)
    - 1 GTC good until canceled
    - 3 IOC immediate or canceled
    - 4 FOK fill or kill — fill the order immediately, or cancel it immediately
    
    There may be other settings for TimeInForce depending on the trading venue
    @type {TimeInForce}
    @memberof CancelReplaceOrderRequest
    '''
    TimeInForce: TimeInForce

    '''
    One Cancels the Other — If the order being canceled in this call is order
    A, and the order replacing order A in this call is order B, then OrderIdOCO refers
    to an order C that is currently open. If order C executes, then order B is canceled.
    You can also set up order C to watch order B in this way, but that will require an
    update to order C.
    @type {number}
    @memberof CancelReplaceOrderRequest
    '''
    OrderIdOCO: Number

    '''
    The amount of the order (buy or sell).
    @type {number}
    @memberof CancelReplaceOrderRequest
    '''
    Quantity: Number


@dataclass
class SendOrderRequest:
    '''
    The ID of the account placing the order.
    @type {number}
    @memberof SendOrderRequest
    '''
    AccountId: Number

    '''
    A user-assigned ID for the order (like a purchase-order number
    assigned by a company). This ID is useful for recognizing future states related to
    this order. ClientOrderId defaults to 0.
    @type {number}
    @memberof SendOrderRequest
    '''
    ClientOrderId: Number

    '''
    The quantity of the instrument being ordered.
    @type {number}
    @memberof SendOrderRequest
    '''
    Quantity: Number

    '''
    The quantity available to buy or sell that is publicly displayed to the market.
    To display a DisplayQuantity value, an order must be a Limit order with a reserve
    @type {number}
    @memberof SendOrderRequest
    '''
    DisplayQuantity: Number

    '''
    If you enter a Limit order with a reserve, you must set UseDisplayQuantity to true
    @type {boolean}
    @memberof SendOrderRequest
    '''
    UseDisplayQuantity: bool

    '''
    The price at which to execute the order, if the order is a Limit order
    @type {number}
    @memberof SendOrderRequest
    '''
    LimitPrice: Number

    '''
    One Cancels the Other — If this order is order A, OrderIdOCO refers to
    the order ID of an order B (which is not the order being created by this call). If
    order B executes, then order A created by this call is canceled. You can also set
    up order B to watch order A in the same way, but that may require an update to
    order B to make it watch this one, which could have implications for priority in the
    order book. See CancelReplaceOrder and ModifyOrder.
    @type {number}
    @memberof SendOrderRequest
    '''
    OrderIdOCO: Number

    '''
    The type of this order, as expressed in integer format. One of:
    - 1 Market
    - 2 Limit
    - 3 StopMarket
    - 4 StopLimit
    - 5 TrailingStopMarket
    - 6 TrailingStopLimit
    - 7 BlockTrade.
    @type {number}
    @memberof SendOrderRequest
    '''
    OrderType: OrderType

    '''
    When entering a stoptrailing order, set PegPriceType to the type of price
    that pegs the stop.
    - 1 Last
    - 2 Bid
    - 3 Ask
    - 4 Midpoint
    @type {PegPriceType}
    @memberof SendOrderRequest
    '''
    PegPriceType: PegPriceType

    '''
    The ID of the instrument being traded in the order
    @type {number}
    @memberof SendOrderRequest
    '''
    InstrumentId: Number

    '''
    The offset by which to trail the market in one of the trailing order types.
    Set this to the current price of the market to ensure that the trailing offset is the
    amount intended in a fast-moving market.
    @type {number}
    @memberof SendOrderRequest
    '''
    TrailingAmount: Number

    '''
    The amount by which a trailing limit order is offset from the activation price.
    @type {number}
    @memberof SendOrderRequest
    '''
    LimitOffset: Number

    '''
    The side of the replacement order:
    - 0 Buy
    - 1 Sell
    - 2 Short (reserved for future use)
    - 3 Unknown (error condition)
    @type {Side}
    @memberof SendOrderRequest
    '''
    Side: Side

    '''
    The price at which to execute the order, if the order is a Stop order
    (either buy or sell).
    @type {number}
    @memberof SendOrderRequest
    '''
    StopPrice: Number

    '''
    The period during which the new order is executable.
    - 0 Unknown (error condition)
    - 1 GTC good until canceled
    - 3 IOC immediate or canceled
    - 4 FOK fill or kill — fill the order immediately, or cancel it immediately
    
    There may be other settings for TimeInForce depending on the trading venue
    
    @type {TimeInForce}
    @memberof SendOrderRequest
    '''
    TimeInForce: TimeInForce

    '''
    The ID of the Order Management System on which the order is being placed.
    @type {number}
    @memberof SendOrderRequest
    '''
    OMSId: Number


@dataclass
class OrderFeeRequest:
    '''
    The ID of the Order Management System on which the trade would take place.
    @type {number}
    @memberof OrderFeeRequest
    '''
    OMSId: Number

    '''
    The ID of the account requesting the fee estimate
    @type {number}
    @memberof OrderFeeRequest
    '''
    AccountId: Number

    '''
    The proposed instrument against which a trading fee would be charged
    @type {number}
    @memberof OrderFeeRequest
    '''
    InstrumentId: Number

    '''
    The ID of the product (currency) in which the fee will be denominated.
    @type {number}
    @memberof OrderFeeRequest
    '''
    ProductId: Number

    '''
    The quantity of the proposed trade for which the Order Management System would charge a fee.
    @type {number}
    @memberof OrderFeeRequest
    '''
    Amount: Number

    '''
    The price at which the proposed trade would take place. Supply your price for a limit order;
    the exact price is difficult to know before execution.
    @type {number}
    @memberof OrderFeeRequest
    '''
    Price: Number

    '''
    The type of the proposed order. One of:
    - 0 Unknown
    - 1 Market
    - 2 Limit
    - 3 StopMarket
    - 4 StopLimit
    - 5 TrailingStopMarket
    - 6 TrailingStopLimit
    - 7 BlockTrade
    @type {OrderType}
    @memberof OrderFeeRequest
    '''
    OrderType: OrderType

    '''
    Depending on the venue, there may be different fees for a maker (the
    order remains on the books for a period) or taker (the order executes directly). If
    the user places a large order that is only partially filled, he is a partial maker.
    - 0 Unknown
    - 1 Maker
    - 2 Taker
    @type {MakerTaker}
    @memberof OrderFeeRequest
    '''
    MakerTaker: MakerTaker


@dataclass
class AllDepositOrWithdrawTicketsRequest:
    '''
    The ID of the Order Management System on which the deposit tickets reside
    @type {number}
    @memberof AllDepositTicketsRequest
    '''
    OMSId: Number

    '''
    The ID of the operator of the trading venue.
    @type {number}
    @memberof AllDepositTicketsRequest
    '''
    OperatorId: Number

    '''
    The ID of the account
    @type {number}
    @memberof AllDepositTicketsRequest
    '''
    AccountId: Number

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
    
    @type {DepositStatus}
    @memberof AllDepositTicketsRequest
    '''
    Status: DepositStatus

    '''
    The ID of a single deposit ticket that is unique across the Order
    Management System. By including a value for TicketId, you limit the returned
    information to a single ticket.
    @type {number}
    @memberof AllDepositTicketsRequest
    '''
    TicketId: Number

    '''
    The start of the period over which to return deposit tickets, in ISO 8601 format.
    @type {string}
    @memberof AllDepositTicketsRequest
    '''
    StartTimestamp: str

    '''
    The end of the period over which to return deposit tickets, in ISO 8601 format
    @type {string}
    @memberof AllDepositTicketsRequest
    '''
    EndTimestamp: str

    '''
    Optional. The deposit ticket at which to start returning the array of
    deposit tickets, starting from 0, the most recent deposit ticket, and working
    backwards in time.
    @type {number}
    @memberof AllDepositTicketsRequest
    '''
    StartIndex: Number

    '''
    Optional. The total number of deposit tickets to return in the array. Limit
    is a 32-bit integer value that can return over 4 billion tickets (4 thousand million).
    If Limit is not specified, all tickets are returned.
    @type {number}
    @memberof AllDepositTicketsRequest
    '''
    Limit: Number

    '''
    The name of the user making the deposit
    @type {string}
    @memberof AllDepositTicketsRequest
    '''
    UserName: str

    '''
    The amount of the deposit. If you specify an Amount value, you must
    include AmountOperator
    @type {number}
    @memberof AllDepositTicketsRequest
    '''
    Amount: Number

    '''
    Tells the response to return tickets in ranges based on the Amount value.
    This stringvalue pair is required if you specify an Amount value. There is no
    AmountOperator setting for greater-than or less-than an Amount value.
    - 0 - returns tickets with values equal to the Amount value.
    - 1 - returns tickets with values equal to or greater than the Amount value.
    - 2 - returns tickets with values less than or equal to the Amount value.
    @type {AmountOperator}
    @memberof AllDepositTicketsRequest
    '''
    AmountOperator: AmountOperator

